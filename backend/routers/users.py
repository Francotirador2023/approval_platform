from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import get_session
from models import User, UserBase, UserRole
from auth import get_password_hash, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# For MVP simplicity, using a custom Create Schema or just body params
from pydantic import BaseModel

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role: UserRole
    email: str
    full_name: str

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User.from_orm(user)
    db_user.password_hash = hashed_password
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

class UserRoleUpdate(BaseModel):
    role: UserRole

@router.get("/", response_model=List[UserRead])
def read_all_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    users = session.exec(select(User)).all()
    return users

@router.put("/{user_id}/role", response_model=UserRead)
def update_user_role(user_id: int, role_update: UserRoleUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.role = role_update.role
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
