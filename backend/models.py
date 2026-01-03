from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str
    role: UserRole = Field(default=UserRole.EMPLOYEE)
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    
    requests: List["Request"] = Relationship(back_populates="requester")
    approvals: List["ApprovalLog"] = Relationship(back_populates="approver")
    notifications: List["Notification"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="author")

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    message: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[int] = Field(default=None, foreign_key="request.id")
    
    user: User = Relationship(back_populates="notifications")
    request: Optional["Request"] = Relationship()

class RequestBase(SQLModel):
    title: str
    description: str
    
class Request(RequestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    requester_id: int = Field(foreign_key="user.id")
    status: RequestStatus = Field(default=RequestStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    requester: User = Relationship(back_populates="requests")
    logs: List["ApprovalLog"] = Relationship(back_populates="request")
    comments: List["Comment"] = Relationship(back_populates="request")

class ApprovalLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="request.id")
    approver_id: int = Field(foreign_key="user.id")
    action: RequestStatus
    comment: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    request: Request = Relationship(back_populates="logs")
    approver: User = Relationship(back_populates="approvals")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="request.id")
    user_id: int = Field(foreign_key="user.id")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    request: Request = Relationship(back_populates="comments")
    author: User = Relationship(back_populates="comments")
