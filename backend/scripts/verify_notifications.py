from sqlmodel import Session, select
from database import engine
from models import Notification, User

def verify_notifications():
    print("Verificando Notificaciones en Base de Datos...\n")
    
    with Session(engine) as session:
        # 1. Check Notifications
        notifications = session.exec(select(Notification).order_by(Notification.created_at.desc()).limit(5)).all()
        
        if not notifications:
            print("No se encontraron notificaciones en la base de datos.")
            return

        print(f"Se encontraron {len(notifications)} notificaciones recientes:")
        for n in notifications:
            # Get user email for context
            user = session.get(User, n.user_id)
            user_email = user.email if user else "Desconocido"
            
            status_icon = "[NO LEIDO]" if not n.is_read else "[LEIDO]"
            print(f"  {status_icon} [ID:{n.id}] Para: {user_email} | Msg: {n.message}")

    print("\nNota: Revisa la consola del servidor (uvicorn) para ver los logs de '--- [MOCK EMAIL] ---' correspondientes.")

if __name__ == "__main__":
    verify_notifications()
