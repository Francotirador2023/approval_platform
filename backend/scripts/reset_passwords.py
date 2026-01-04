
import sys
import os

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from sqlmodel import Session, select
from database import engine
from models import User
from auth import get_password_hash

def reset_passwords():
    print("--- Resetting Passwords ---")
    with Session(engine) as session:
        users_to_reset = ["manager@example.com", "francojonysenati@gmail.com", "admin@example.com"]
        for email in users_to_reset:
            user = session.exec(select(User).where(User.email == email)).first()
            if user:
                # Reset to '123456'
                user.password_hash = get_password_hash("123456")
                session.add(user)
                print(f"Password for {email} reset to '123456'")
            else:
                print(f"User {email} not found")
        
        session.commit()
        print("Done.")

if __name__ == "__main__":
    reset_passwords()
