import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool
from main import app
from database import get_session
from models import User, UserRole, Request, RequestStatus
from auth import get_current_user

# Setup in-memory DB
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_request_sends_email(client: TestClient, session: Session):
    # Setup users
    manager = User(email="manager@example.com", full_name="Manager User", role=UserRole.MANAGER, password_hash="hash")
    employee = User(email="employee@example.com", full_name="Employee User", role=UserRole.EMPLOYEE, password_hash="hash")
    session.add(manager)
    session.add(employee)
    session.commit()
    session.refresh(manager)
    session.refresh(employee)
    
    # Mock auth to be employee
    app.dependency_overrides[get_current_user] = lambda: employee

    # Mock send_email
    with patch("routers.requests.send_email") as mock_send_email:
        response = client.post("/requests/", json={"title": "Test Req", "description": "Desc"})
        # Print output if fail
        if response.status_code != 200:
             print(response.content)
        assert response.status_code == 200
        
        # Verify email was sent to manager
        mock_send_email.assert_called_once()
        # call_args could be args or kwargs. 
        # Integration code: send_email(to_email=..., subject=..., body=...)
        call_args = mock_send_email.call_args
        kwargs = call_args.kwargs
        args = call_args.args
        
        to = kwargs.get("to_email") or (args[0] if args else None)
        subject = kwargs.get("subject") or (args[1] if len(args) > 1 else None)
        
        assert to == "manager@example.com"
        assert "Nueva Solicitud" in subject

def test_update_status_sends_email(client: TestClient, session: Session):
    # Setup users
    manager = User(email="manager@example.com", full_name="Manager User", role=UserRole.MANAGER, password_hash="hash")
    employee = User(email="employee@example.com", full_name="Employee User", role=UserRole.EMPLOYEE, password_hash="hash")
    session.add(manager)
    session.add(employee)
    session.commit()
    session.refresh(manager)
    session.refresh(employee)
    
    # Create request
    req = Request(title="Test Req", description="Desc", requester_id=employee.id, status=RequestStatus.PENDING)
    session.add(req)
    session.commit()
    
    # Mock auth to be manager
    app.dependency_overrides[get_current_user] = lambda: manager
    
    # Mock send_email
    with patch("routers.requests.send_email") as mock_send_email:
        response = client.put(f"/requests/{req.id}/status", json={"status": "approved", "comment": "Good"})
        assert response.status_code == 200
        
        # Verify email sent to employee
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        kwargs = call_args.kwargs
        args = call_args.args
        
        to = kwargs.get("to_email") or (args[0] if args else None)
        subject = kwargs.get("subject") or (args[1] if len(args) > 1 else None)
        
        assert to == "employee@example.com"
        assert "Actualización de Solicitud" in subject

def test_process_email_requests_creates_request(session: Session):
    from email_service import process_email_requests
    
    # Setup user
    user = User(email="sender@example.com", full_name="Sender", role=UserRole.EMPLOYEE, password_hash="hash")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Mock MailBox
    with patch("email_service.MailBox") as MockMailBox:
        # Configure mock to return a context manager
        mock_mailbox_instance = MockMailBox.return_value
        mock_mailbox_instance.__enter__.return_value = mock_mailbox_instance
        
        # Create a mock email object
        mock_email = MagicMock()
        mock_email.from_ = "sender@example.com"
        mock_email.subject = "New Request via Email"
        mock_email.text = "Description from email body"
        mock_email.html = None
        
        # Configure fetch to return our mock email
        mock_mailbox_instance.fetch.return_value = [mock_email]
        
        # Override dependency or ensure email_service uses the same engine/session logic
        # email_service.py uses its own 'engine' import. We need to patch 'email_service.Session' 
        # to return our test 'session' or patch 'email_service.engine'.
        # EASIER: Patch 'email_service.Session' to be a context manager yielding our session
        with patch("email_service.Session") as MockSession:
            MockSession.return_value.__enter__.return_value = session
            
            # Run function
            stats = process_email_requests()
            
            # Assert Request created
            req = session.exec(select(Request).where(Request.title == "New Request via Email")).first()
            assert req is not None
            assert req.description == "Description from email body"
            assert req.requester_id == user.id
            assert req.status == RequestStatus.PENDING
            
            # Verify stats
            assert stats["processed"] == 1
            assert stats["created"] == 1
            assert stats["skipped"] == 0
