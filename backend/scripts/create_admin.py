import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User, UserRole
from auth import get_password_hash

def create_admin_user():
    create_db_and_tables()
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "admin@example.com")).first()
        if not user:
            print("Creating admin user...")
            admin_user = User(
                email="admin@example.com",
                full_name="Admin User",
                password_hash=get_password_hash("admin123"),
                role=UserRole.ADMIN
            )
            session.add(admin_user)
            session.commit()
            print("Admin user created: admin@example.com / admin123")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    create_admin_user()
