
import sys
import os
from unittest.mock import patch, MagicMock
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

# Imports from same dir
from models import User, UserRole, Request, RequestStatus
from email_service import process_email_requests

# Setup DB
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
SQLModel.metadata.create_all(engine)

def test_sync():
    print("Setting up test data...")
    with Session(engine) as session:
        user = User(email="sender@example.com", full_name="Sender", role=UserRole.EMPLOYEE, password_hash="hash")
        session.add(user)
        session.commit()
        session.refresh(user)

    print("Mocking dependencies...")
    # Mock MailBox
    with patch("email_service.MailBox") as MockMailBox:
        mock_mailbox_instance = MockMailBox.return_value
        mock_mailbox_instance.login.return_value = mock_mailbox_instance # Fix: login must return self
        mock_mailbox_instance.__enter__.return_value = mock_mailbox_instance
        
        mock_email = MagicMock()
        mock_email.from_ = "sender@example.com"
        mock_email.subject = "New Request via Email"
        mock_email.text = "Description from email body"
        mock_email.html = None
        
        # Return 1 email
        mock_mailbox_instance.fetch.return_value = [mock_email]
        
        # Patch EMAIL_ACCOUNT constant in email_service
        with patch("email_service.EMAIL_ACCOUNT", "real@example.com"):
            # Patch Session to use our test DB
            with patch("email_service.Session") as MockSession:
                MockSession.return_value.__enter__.return_value = Session(engine)
                
                print("Running process_email_requests...")
                stats = process_email_requests()
                print(f"Stats returned: {stats}")
                
                if stats["processed"] == 1 and stats["created"] == 1 and stats["skipped"] == 0:
                    print("SUCCESS: Stats are correct!")
                else:
                    print(f"FAILURE: Stats are incorrect. Got: {stats}")
                    sys.exit(1)

if __name__ == "__main__":
    test_sync()
