from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User, UserRole
from auth import get_password_hash
import sys
import os

# Add parent to path if run from scripts dir
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_test_user():
    print("--- Creador de Usuarios de Prueba ---")
    email = input("Introduce el correo que usarás para enviar la prueba: ").strip()
    if not email:
        print("Correo no válido.")
        return

    name = input("Introduce un nombre para este usuario: ").strip()
    password = "password123" # Default password for simplicity

    create_db_and_tables()
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            print(f"¡El usuario {email} ya existe!")
            return

        new_user = User(
            email=email,
            full_name=name,
            password_hash=get_password_hash(password),
            role=UserRole.EMPLOYEE
        )
        session.add(new_user)
        session.commit()
        print(f"\n[ÉXITO] Usuario creado: {email}")
        print(f"Contraseña por defecto: {password}")
        print("Ahora puedes enviar correos desde esa dirección y serán procesados.")

if __name__ == "__main__":
    create_test_user()
