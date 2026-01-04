
import sys
import os

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from sqlmodel import Session, select
from database import engine
from models import User, UserRole
from auth import get_password_hash

def add_manager():
    print("--- Adding Manager ---")
    email = "manager@example.com"
    password = "123456"
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            print(f"User {email} already exists")
            user.password_hash = get_password_hash(password)
            session.add(user)
            session.commit()
            print("Password reset.")
            return

        new_user = User(
            email=email,
            full_name="Admin Manager",
            password_hash=get_password_hash(password),
            role=UserRole.MANAGER
        )
        session.add(new_user)
        session.commit()
        print(f"User created: {email}")

if __name__ == "__main__":
    add_manager()
