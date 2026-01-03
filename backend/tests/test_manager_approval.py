import urllib.request
import urllib.parse
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8001"

def get_auth_token(email, password):
    url = f"{BASE_URL}/auth/token"
    # OAuth2 form-encoded
    data = urllib.parse.urlencode({
        "username": email,
        "password": password
    }).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode()
            return json.loads(body)["access_token"]
    except Exception as e:
        print(f"Failed to login as {email}: {e}")
        return None

def create_request(token, title):
    url = f"{BASE_URL}/requests/"
    data = json.dumps({
        "title": title,
        "description": "Auto-generated for approval test"
    }).encode()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Failed to create request: {e}")
        return None

def test_approve_request():
    # 0. Login as Employee to create a request
    print("Logging in as Employee...")
    emp_token = get_auth_token("emp@example.com", "emp123")
    if not emp_token:
        print("Employee login failed")
        return

    print("Creating request 'Request for Approval'...")
    new_req = create_request(emp_token, "Request for Approval")
    if not new_req:
        return
    print(f"Created Request ID: {new_req['id']}")
    
    # 1. Login as Manager
    print("\nLogging in as Manager...")
    mgr_token = get_auth_token("admin@example.com", "admin123")
    if not mgr_token: 
        print("Manager login failed")
        return

    headers = {
        "Authorization": f"Bearer {mgr_token}",
        "Content-Type": "application/json"
    }

    # 2. Approve it directly (we have the ID)
    request_id = new_req['id']
    print(f"\nApproving Request {request_id}...")
    update_url = f"{BASE_URL}/requests/{request_id}/status"
    data = json.dumps({
        "status": "approved",
        "comment": "LGTM from script auto-test"
    }).encode()
    
    req = urllib.request.Request(update_url, data=data, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Update Status: {response.getcode()}")
            updated_req = json.loads(response.read().decode())
            print(f"New Status: {updated_req['status']}")
    except urllib.error.HTTPError as e:
        print(f"Update Failed: {e.code} - {e.read().decode()}")

if __name__ == "__main__":
    test_approve_request()

