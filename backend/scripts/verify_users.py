from sqlmodel import Session, select
from database import engine
from models import User
from auth import verify_password

def verify_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print(f"Total users found: {len(users)}")
        for user in users:
            print(f"User: {user.email}, Role: {user.role}, Hash: {user.password_hash[:10]}...")
            
            # Test passwords
            if user.email == "emp@example.com":
                is_valid = verify_password("emp123", user.password_hash)
                print(f"  Password 'emp123' valid? {is_valid}")
            elif user.email == "admin@example.com":
                is_valid = verify_password("admin123", user.password_hash)
                print(f"  Password 'admin123' valid? {is_valid}")

if __name__ == "__main__":
    verify_users()
