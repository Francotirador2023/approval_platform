from sqlmodel import Session, select
from database import engine
from models import User

def check_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print(f"Total Users: {len(users)}")
        for u in users:
            print(f"- {u.email} (Role: {u.role}, Hash: {u.password_hash[:10]}...)")

if __name__ == "__main__":
    check_users()
