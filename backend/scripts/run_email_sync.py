import sys
import os
import time
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env vars from parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from email_service import process_email_requests
from database import create_db_and_tables

def main():
    print("--- Iniciando Sincronización de Correos ---")
    print("Buscando correos no leídos para convertir en solicitudes...")
    
    # Ensure DB exists
    create_db_and_tables()
    
    try:
        process_email_requests()
        print("--- Sincronización Finalizada ---")
    except Exception as e:
        print(f"Error durante la sincronización: {e}")

if __name__ == "__main__":
    main()
