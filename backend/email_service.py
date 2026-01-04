import os
from imap_tools import MailBox, AND
from sqlmodel import Session, select
from database import engine
from models import User, Request, RequestStatus
from auth import get_password_hash # If we need to create users

# Configuration
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "test@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "password")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using SMTP.
    If credentials are 'test@example.com' (default), it logs to console instead.
    """
    if EMAIL_ACCOUNT == "test@example.com" or not EMAIL_PASSWORD:
        print(f"--- [MOCK EMAIL] ---\nTo: {to_email}\nSubject: {subject}\nBody: {body}\n--------------------")
        return

    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ACCOUNT
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server
        # Assuming Gmail for now based on IMAP default, but easily configurable
        smtp_server = "smtp.gmail.com" 
        smtp_port = 587
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
            server.send_message(msg)
            
        print(f"Email sent to {to_email}")
        
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")


def process_email_requests():
    """
    Connect to IMAP, fetch UNSEEN emails, and create requests.
    Returns a dict with statistics: {'processed': int, 'created': int, 'skipped': int, 'errors': list}
    """
    stats = {
        "processed": 0,
        "created": 0,
        "skipped": 0,
        "errors": []
    }

    if EMAIL_ACCOUNT == "test@example.com":
        print("Email integration skipped: No valid credentials provided.")
        stats["errors"].append("Email integration skipped: No valid credentials provided.")
        return stats

    try:
        with MailBox(IMAP_SERVER).login(EMAIL_ACCOUNT, EMAIL_PASSWORD) as mailbox:
            # Fetch unseen emails, limit to 50 recent
            for msg in mailbox.fetch(AND(seen=False), limit=50, reverse=True):
                stats["processed"] += 1
                try:
                    print(f"DEBUG SYNC: Processing email from '[{msg.from_}]' Subject: '{msg.subject}'", flush=True)
                    
                    # Check if user exists by email helper (case-insensitive)
                    sender_email = msg.from_.strip().lower()
                    
                    with Session(engine) as session:
                        # Use ilike for case-insensitive match if supported, or just compare in python for safety with SQLite
                        # SQLite default collation might be case insensitive but let's be explicit
                        statement = select(User).where(User.email == sender_email)
                        user = session.exec(statement).first()
                        
                        if not user:
                            # Try finding without lower() just in case DB has mixed case
                            user = session.exec(select(User).where(User.email == msg.from_.strip())).first()

                        if not user:
                            print(f"DEBUG SYNC: User '{sender_email}' not found in DB. Skipping.", flush=True)
                            stats["skipped"] += 1
                            continue
                        
                        print(f"DEBUG SYNC: User found: {user.email}", flush=True)
                            
                        # Create Request
                        new_request = Request(
                            title=msg.subject,
                            description=msg.text or msg.html or "No content",
                            requester_id=user.id,
                            status=RequestStatus.PENDING
                        )
                        session.add(new_request)
                        session.commit()
                        print(f"Request created: {new_request.id}")
                        stats["created"] += 1
                except Exception as inner_e:
                    print(f"Error processing specific email: {inner_e}")
                    stats["errors"].append(f"Error processing email from {msg.from_}: {str(inner_e)}")
                    
    except Exception as e:
        print(f"Error processing emails: {e}")
        stats["errors"].append(f"Global error: {str(e)}")
    
    return stats
