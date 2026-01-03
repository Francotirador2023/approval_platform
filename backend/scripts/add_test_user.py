import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User, UserRole
from auth import get_password_hash

def add_user():
    email = "francojonysenati@gmail.com"
    full_name = "Franco Jony"
    password = "password123"
    
    with Session(engine) as session:
        # Check if exists
        state = session.exec(select(User).where(User.email == email)).first()
        if state:
            print(f"El usuario {email} ya existe.")
            return

        new_user = User(
            email=email,
            full_name=full_name,
            role=UserRole.EMPLOYEE,
            password_hash=get_password_hash(password)
        )
        session.add(new_user)
        session.commit()
        print(f"Usuario creado exitosamente: {email} / {password}")

if __name__ == "__main__":
    create_db_and_tables()
    add_user()
