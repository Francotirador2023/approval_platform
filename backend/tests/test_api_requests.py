import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8001"

def get_auth_token(email, password):
    url = f"{BASE_URL}/auth/token"
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

def verify_requests_list():
    # 1. Login as Admin
    print("Logging in as Admin...")
    token = get_auth_token("admin@example.com", "admin123")
    if not token: 
        print("Login failed")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 2. List Requests
    print("\nListing Requests...")
    list_url = f"{BASE_URL}/requests/"
    req = urllib.request.Request(list_url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"List Status: {response.getcode()}")
            requests = json.loads(response.read().decode())
            print(f"Found {len(requests)} requests")
            for r in requests:
                print(f" - [{r['status']}] ID:{r['id']} '{r['title']}' (by {r['requester_name']})")
    except urllib.error.HTTPError as e:
        print(f"List Failed: {e.code} - {e.read().decode()}")

if __name__ == "__main__":
    verify_requests_list()
