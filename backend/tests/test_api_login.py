import urllib.request
import urllib.parse
import json

def test_login():
    url = "http://127.0.0.1:8001/auth/token"
    # OAuth2 form-encoded data
    data = urllib.parse.urlencode({
        "username": "emp@example.com",
        "password": "emp123"
    }).encode()
    
    req = urllib.request.Request(url, data=data, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            body = response.read().decode()
            print(f"Status Code: {status_code}")
            print(f"Response: {body}")
            
            data = json.loads(body)
            token = data.get("access_token")
            print(f"Success! Token: {token[:10]}...")
            
            # Verify /users/me
            me_url = "http://127.0.0.1:8001/users/me"
            headers = {"Authorization": f"Bearer {token}"}
            me_req = urllib.request.Request(me_url, headers=headers)
            with urllib.request.urlopen(me_req) as me_response:
                print(f"User Me Status: {me_response.getcode()}")
                print(f"User Me Response: {me_response.read().decode()}")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(e.read().decode())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
