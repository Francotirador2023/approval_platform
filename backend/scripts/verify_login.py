
import sys
import os

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from sqlmodel import Session, select
from database import engine
from models import User
from auth import verify_password

def check_login():
    print("--- Verifying Login ---")
    print(f"DB URL: {engine.url}")
    email = "manager@example.com"
    password = "123456"
    
    with Session(engine) as session:
        all_users = session.exec(select(User)).all()
        print(f"Total users in DB: {len(all_users)}")
        for u in all_users:
            print(f" - {u.email} (Rol: {u.role})")
            
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            print(f"CRITICAL: User {email} not found in this DB connection!")
            return

        print(f"User found: {user.email}")
        
        is_valid = verify_password(password, user.password_hash)
        if is_valid:
            print("LOGIN SUCCESS: Password is correct.")
        else:
            print("LOGIN FAILED: Password mismatch.")

if __name__ == "__main__":
    check_login()
