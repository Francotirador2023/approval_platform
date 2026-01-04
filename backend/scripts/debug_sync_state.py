
import sys
import os
from imap_tools import MailBox, AND

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from sqlmodel import Session, select
from database import engine
from models import User
from dotenv import load_dotenv

dotenv_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path)

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def debug_state():
    print("--- DEBUGGING SYNC STATE ---")
    
    # 1. Check DB User
    with Session(engine) as session:
        target_email = "francojonysenati@gmail.com"
        user = session.exec(select(User).where(User.email == target_email)).first()
        if user:
            print(f"[DB] User found: {user.email} (ID: {user.id})")
        else:
            print(f"[DB] CRITICAL: User {target_email} NOT FOUND in DB!")

    # 2. Check Email Server
    print(f"\n[IMAP] Connecting to {IMAP_SERVER} as {EMAIL_ACCOUNT}...")
    try:
        with MailBox(IMAP_SERVER).login(EMAIL_ACCOUNT, EMAIL_PASSWORD) as mailbox:
            print("[IMAP] Login Successful.")
            
            # List last 10 emails (ANY status) to see what's there
            print("\n[IMAP] Checking last 10 emails (SEEN and UNSEEN):")
            for msg in mailbox.fetch(limit=10, reverse=True):
                status = "SEEN" if 'SEEN' in msg.flags else "UNSEEN"
                print(f" - From: {msg.from_} | Subject: {msg.subject} | Status: {status}")
                
    except Exception as e:
        print(f"[IMAP] Error: {e}")

if __name__ == "__main__":
    debug_state()
