import sys
import os

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User, UserRole
from auth import get_password_hash

def add_user():
    print("--- Adding User Automatically ---")
    email = "francojonysenati@gmail.com"
    name = "Jony Dev"
    password = "password123"

    create_db_and_tables()
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            print(f"User {email} already exists!")
            return

        new_user = User(
            email=email,
            full_name=name,
            password_hash=get_password_hash(password),
            role=UserRole.EMPLOYEE
        )
        session.add(new_user)
        session.commit()
        print(f"User created: {email}")

if __name__ == "__main__":
    add_user()
