from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import auth, users, requests, notifications
from email_service import process_email_requests

app = FastAPI(title="Approval Platform MVP")

# CORS setup
import os

# CORS setup
# Read from env or default to Vite's default ports
origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174")
origins = [origin.strip() for origin in origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(requests.router)
app.include_router(notifications.router)

@app.post("/sync-emails")
async def sync_emails_endpoint():
    """
    Trigger email synchronization manually.
    """
    try:
        stats = process_email_requests()
        return {"message": "Email synchronization completed", "stats": stats}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Approval Platform API"}
