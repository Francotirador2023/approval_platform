
import imaplib
import os
import sys

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from dotenv import load_dotenv

# Load env from backend/.env
dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path)

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def check_imap():
    print(f"Testing connection to {IMAP_SERVER} for {EMAIL_ACCOUNT}...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        print("LOGIN SUCCESSFUL!")
        
        mail.select('inbox')
        status, messages = mail.search(None, 'UNSEEN')
        raw_ids = messages[0]
        id_list = raw_ids.split()
        print(f"DEBUG: Status={status}, Raw IDs={raw_ids}", flush=True)
        print(f"!!! UNREAD COUNT: {len(id_list)} !!!", flush=True)
        
        mail.logout()
    except Exception as e:
        print(f"LOGIN FAILED: {e}", flush=True)

if __name__ == "__main__":
    check_imap()
