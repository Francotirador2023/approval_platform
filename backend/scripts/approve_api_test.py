import urllib.request
import urllib.parse
import json
import ssl
from sqlmodel import Session, select
from database import engine
from models import Request, RequestStatus
# Models import might fail if running outside venv context correctly but we use venv python so okay.

def run():
    # 1. Login
    login_url = "http://127.0.0.1:8001/auth/token"
    data = urllib.parse.urlencode({"username": "admin@example.com", "password": "admin123"}).encode()
    req = urllib.request.Request(login_url, data=data, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.load(response)
            token = res_json["access_token"]
    except Exception as e:
        print(f"Login failed: {e}")
        return

    print("Login successful.")

    # 2. Get Request ID
    # Reuse previous logic or just select manually
    # We will assume we can import models because we are in backend dir
    with Session(engine) as session:
        r = session.exec(select(Request).where(Request.status == "pending").order_by(Request.id.desc())).first()
        if not r:
            print("No pending request.")
            return
        req_id = r.id
    
    print(f"Approving Request {req_id}")

    # 3. Approve
    approve_url = f"http://127.0.0.1:8001/requests/{req_id}/status"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = json.dumps({"status": "approved", "comment": "API Test"}).encode()
    
    req = urllib.request.Request(approve_url, data=body, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("Approval API success.")
                print(response.read().decode())
    except urllib.error.HTTPError as e:
         print(f"Approval failed: {e.code} {e.read().decode()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
