# Plataforma de Aprobación

Sistema de gestión de solicitudes y aprobaciones (MVP).

## Características
- **Roles**: Empleado (crea solicitudes), Gerente/Admin (aprueba/rechaza).
- **Notificaciones**: Alertas en tiempo real y correos electrónicos (simulados por defecto).
- **Idioma**: Completamente en español.

## Estructura del Proyecto
- `backend/`: API REST construida con FastAPI y SQLModel.
- `frontend/`: Interfaz de usuario React construida con Vite.

## Requisitos Previos
- Python 3.9+
- Node.js 16+

## Instalación y Ejecución

### 1. Iniciar el Backend
Desde la carpeta raíz del proyecto:

```bash
cd backend
# Crear entorno virtual (si no existe)
python -m venv venv
# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python -m uvicorn main:app --reload
```
El backend estará disponible en `http://127.0.0.1:8000`.

### 2. Iniciar el Frontend
En una nueva terminal:

```bash
cd frontend
# Instalar dependencias (primera vez)
npm install

# Iniciar servidor de desarrollo
npm run dev
```
El frontend estará disponible en `http://localhost:5173`.

## Usuarios de Prueba (Seed)
El sistema incluye usuarios predefinidos:

- **Empleado**: `emp@example.com` / `emp123`
- **Gerente**: `manager@example.com` / `manager123`
- **Admin**: `admin@example.com` / `admin123`

## Scripts de Utilidad
En la carpeta `backend/scripts/`:
- `verify_full_flow.py`: Ejecuta una prueba automática de todo el flujo.
- `seed.py`: Reinicia la base de datos con datos de prueba.

---
**Nota**: Los correos electrónicos se imprimen en la consola del backend por defecto. Para configurar SMTP real, edite `backend/email_service.py`.
