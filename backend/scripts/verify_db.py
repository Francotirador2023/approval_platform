from sqlmodel import Session, select
from database import engine
from models import Request, RequestStatus

def check_latest_request():
    with Session(engine) as session:
        request = session.exec(select(Request).order_by(Request.id.desc())).first()
        if request:
            print(f"Latest Request ID: {request.id}")
            print(f"Title: {request.title}")
            print(f"Status: {request.status}")
        else:
            print("No requests found.")

if __name__ == "__main__":
    check_latest_request()
