from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from database import get_session
from models import Notification, User
from auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/notifications", tags=["notifications"])

class NotificationRead(BaseModel):
    id: int
    message: str
    is_read: bool
    created_at: datetime
    request_id: int | None

@router.get("/", response_model=List[NotificationRead])
def get_notifications(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Return unread notifications first, then recent read ones. limit to 20.
    query = select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.is_read, Notification.created_at.desc()).limit(20)
    return session.exec(query).all()

@router.put("/{notification_id}/read")
def mark_notification_read(notification_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    notification.is_read = True
    session.add(notification)
    session.commit()
    return {"message": "Marked as read"}
