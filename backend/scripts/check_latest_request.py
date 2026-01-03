from sqlmodel import Session, select, create_engine
from models import Request, User
from database import engine

def check_latest():
    with Session(engine) as session:
        statement = select(Request).order_by(Request.id.desc()).limit(1)
        result = session.exec(statement).first()
        if result:
            print(f"Latest Request: ID={result.id} Title='{result.title}' Status={result.status}")
        else:
            print("No requests found.")

if __name__ == "__main__":
    check_latest()
