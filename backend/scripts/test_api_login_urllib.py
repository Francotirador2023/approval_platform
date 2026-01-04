
import urllib.request
import urllib.parse
import json

def test_login():
    url = "http://localhost:8000/auth/token"
    payload = {
        "username": "manager@example.com",
        "password": "123456"
    }
    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    
    # Headers
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    print(f"POST {url}")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Status Code: {response.getcode()}")
            print(f"Response: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(f"Reason: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
