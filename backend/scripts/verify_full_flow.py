import urllib.request
import urllib.parse
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8001"

def get_auth_token(email, password):
    url = f"{BASE_URL}/auth/token"
    data = urllib.parse.urlencode({
        "username": email,
        "password": password
    }).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode()
            return json.loads(body)["access_token"]
    except Exception as e:
        print(f"❌ Fallo al iniciar sesión como {email}: {e}")
        return None

def verify_full_flow():
    print("Iniciando Verificacion de Flujo Completo...\n")

    # 1. Login as Employee
    print("1. Iniciando sesion como Empleado (emp@example.com)...")
    emp_token = get_auth_token("emp@example.com", "emp123")
    if not emp_token: return

    # 2. Create Request
    print("2. Creando Nueva Solicitud...")
    create_url = f"{BASE_URL}/requests/"
    
    req_data = json.dumps({
        "title": f"Verificacion Auto {int(time.time())}",
        "description": "Esta es una solicitud de prueba automatica para verificar el flujo completo."
    }).encode()

    headers_emp = {
        "Authorization": f"Bearer {emp_token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(create_url, data=req_data, headers=headers_emp, method="POST")
        with urllib.request.urlopen(req) as response:
            new_req = json.loads(response.read().decode())
            req_id = new_req["id"]
            print(f"Solicitud Creada con ID: {req_id}")
    except Exception as e:
        print(f"Error creando solicitud: {e}")
        return

    # 3. Login as Manager
    print("\n3. Iniciando sesion como Manager (admin@example.com)...")
    mgr_token = get_auth_token("admin@example.com", "admin123")
    if not mgr_token: return

    # 4. Approve Request
    print(f"4. Aprobando Solicitud {req_id}...")
    approve_url = f"{BASE_URL}/requests/{req_id}/status"
    
    approve_data = json.dumps({
        "status": "approved",
        "comment": "Aprobado automaticamente por script de verificacion."
    }).encode()

    headers_mgr = {
        "Authorization": f"Bearer {mgr_token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(approve_url, data=approve_data, headers=headers_mgr, method="PUT")
        with urllib.request.urlopen(req) as response:
            updated_req = json.loads(response.read().decode())
            print(f"Estado Actualizado: {updated_req['status']}")
            
            if updated_req['status'] == 'approved':
                print("\nEXITO! El flujo completo de solicitud y aprobacion funciona correctamente.")
            else:
                print("\nALERTA: La solicitud no aparece como aprobada.")
    except Exception as e:
        print(f"Error aprobando solicitud: {e}")

if __name__ == "__main__":
    verify_full_flow()
