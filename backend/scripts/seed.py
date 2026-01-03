from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User, UserRole
from auth import get_password_hash

def seed_users():
    create_db_and_tables()
    with Session(engine) as session:
        # Check if admin exists
        user = session.exec(select(User).where(User.email == "admin@example.com")).first()
        if not user:
            admin = User(
                email="admin@example.com",
                full_name="Admin User",
                role=UserRole.ADMIN,
                password_hash=get_password_hash("admin123")
            )
            session.add(admin)
            print("Created Admin User: admin@example.com / admin123")

        # Check if employee exists
        user = session.exec(select(User).where(User.email == "emp@example.com")).first()
        if not user:
            emp = User(
                email="emp@example.com",
                full_name="John Employee",
                role=UserRole.EMPLOYEE,
                password_hash=get_password_hash("emp123")
            )
            session.add(emp)
            print("Created Employee User: emp@example.com / emp123")
        
        session.commit()

if __name__ == "__main__":
    seed_users()
