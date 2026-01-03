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
    Using imap-tools for simplicity.
    """
    if EMAIL_ACCOUNT == "test@example.com":
        print("Email integration skipped: No valid credentials provided.")
        return

    try:
        with MailBox(IMAP_SERVER).login(EMAIL_ACCOUNT, EMAIL_PASSWORD) as mailbox:
            # Fetch unseen emails
            for msg in mailbox.fetch(AND(seen=False)):
                print(f"Processing email from {msg.from_} subject: {msg.subject}")
                
                # Check if user exists by email helper
                sender_email = msg.from_
                
                with Session(engine) as session:
                    user = session.exec(select(User).where(User.email == sender_email)).first()
                    
                    if not user:
                        # Optional: Auto-create user or skip
                        print(f"User {sender_email} not found. Skipping.")
                        continue
                        
                    # Create Request
                    new_request = Request(
                        title=msg.subject,
                        description=msg.text or msg.html,
                        requester_id=user.id,
                        status=RequestStatus.PENDING
                    )
                    session.add(new_request)
                    session.commit()
                    print(f"Request created: {new_request.id}")
                    
    except Exception as e:
        print(f"Error processing emails: {e}")
