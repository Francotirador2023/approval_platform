from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from database import get_session
from models import Request, RequestBase, RequestStatus, User, UserRole, ApprovalLog, Notification, Comment
from auth import get_current_user
from email_service import send_email # Absolute import via sys.path or relative if package structure supports it. 
# However, usually FastAPI runs from backend root. Let's check imports.
# backend/main.py usually runs uvicorn. 
# "from email_service" might work if running from backend dir.
# But inside routers/requests.py, we might need "from ..email_service import send_email" if imported as module.
# Let's rely on standard python path behavior if running from backend root:
# from email_service import send_email


from pydantic import BaseModel

router = APIRouter(prefix="/requests", tags=["requests"])

class RequestCreate(RequestBase):
    pass

class ApprovalLogRead(BaseModel):
    action: RequestStatus
    comment: Optional[str]
    timestamp: datetime
    approver_name: str

class RequestRead(RequestBase):
    id: int
    requester_id: int
    status: RequestStatus
    created_at: datetime
    requester_name: str 
    logs: List[ApprovalLogRead] = [] 

class RequestUpdateStatus(BaseModel):
    status: RequestStatus
    comment: Optional[str] = None

@router.post("/", response_model=RequestRead)
def create_request(
    request: RequestCreate, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    db_request = Request(**request.model_dump(), requester_id=current_user.id)
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    
    # Notify all managers
    managers = session.exec(select(User).where(User.role == UserRole.MANAGER)).all()
    # Fallback: if no managers, notify admins
    if not managers:
        managers = session.exec(select(User).where(User.role == UserRole.ADMIN)).all()
        
    for manager in managers:
        # Don't notify self if manager creates request
        if manager.id != current_user.id:
            notification = Notification(
                user_id=manager.id,
                message=f"Nueva solicitud de {current_user.full_name}: {db_request.title}",
                request_id=db_request.id
            )
            session.add(notification)
            
            # Send Email (Background)
            background_tasks.add_task(
                send_email,
                to_email=manager.email,
                subject=f"Nueva Solicitud: {db_request.title}",
                body=f"Hola {manager.full_name},\n\n{current_user.full_name} ha enviado una nueva solicitud: '{db_request.title}'.\n\nPor favor inicie sesión para revisarla."
            )
    
    session.commit() # Commit notifications
    
    return RequestRead(
        id=db_request.id,
        title=db_request.title,
        description=db_request.description,
        requester_id=db_request.requester_id,
        status=db_request.status,
        created_at=db_request.created_at,
        requester_name=current_user.full_name,
        logs=[]
    )

@router.get("/", response_model=List[RequestRead])
def read_requests(
    status_filter: Optional[RequestStatus] = None, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    query = select(Request)
    
    # If not manager/admin, only see own requests
    if current_user.role == UserRole.EMPLOYEE:
        query = query.where(Request.requester_id == current_user.id)
    
    if status_filter:
        query = query.where(Request.status == status_filter)
        
    requests = session.exec(query).all()
    
    # Enrich with requester name (optimize via join in real app)
    result = []
    for req in requests:
        # Enrich logs
        logs_read = []
        for log in req.logs:
            logs_read.append(ApprovalLogRead(
                action=log.action,
                comment=log.comment,
                timestamp=log.timestamp,
                approver_name=log.approver.full_name if log.approver else "Unknown"
            ))
            
        # Lazy loading requester if not joined
        requester_name = req.requester.full_name if req.requester else "Unknown"
        
        result.append(RequestRead(
            id=req.id,
            title=req.title,
            description=req.description,
            requester_id=req.requester_id,
            status=req.status,
            created_at=req.created_at, 
            requester_name=requester_name,
            logs=logs_read
        ))
        
    return result

@router.put("/{request_id}/status", response_model=RequestRead)
def update_request_status(
    request_id: int, 
    update_data: RequestUpdateStatus, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    req = session.get(Request, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
    # Only managers/admins can approve/reject
    if current_user.role == UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="No autorizado para aprobar/rechazar solicitudes")
        
    req.status = update_data.status
    session.add(req)
    
    # Log the action
    log = ApprovalLog(
        request_id=req.id,
        approver_id=current_user.id,
        action=update_data.status,
        comment=update_data.comment
    )
    session.add(log)
    
    # Notify the requester
    notification = Notification(
        user_id=req.requester_id,
        message=f"Tu solicitud '{req.title}' ha sido marcada como {update_data.status.value}",
        request_id=req.id
    )
    session.add(notification)
    
    # Send Email to requester
    requester = session.get(User, req.requester_id)
    if requester:
        background_tasks.add_task(
            send_email,
            to_email=requester.email,
            subject=f"Actualización de Solicitud: {req.title}",
            body=f"Hola {requester.full_name},\n\nTu solicitud '{req.title}' ha sido marcada como {update_data.status.value}.\n\nComentario: {update_data.comment or 'Sin comentarios.'}"
        )

    session.commit()
    session.refresh(req)
    session.refresh(req)
    # Re-fetch or manually construct logs to return complete object
    logs_read = []
    for l in req.logs:
         logs_read.append(ApprovalLogRead(
                action=l.action,
                comment=l.comment,
                timestamp=l.timestamp,
                approver_name=l.approver.full_name if l.approver else "Unknown"
            ))
            
    return RequestRead(
        id=req.id,
        title=req.title,
        description=req.description,
        requester_id=req.requester_id,
        status=req.status,
        created_at=req.created_at,
        requester_name=req.requester.full_name,
        logs=logs_read
    )
