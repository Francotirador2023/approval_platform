# Guía de Despliegue a Producción

Esta guía describe los pasos necesarios para llevar la Plataforma de Aprobación a un entorno de producción.

## 1. Backend (FastAPI)

### Preparación
1.  **Variables de Entorno**:
    Copia el archivo `.env.example` a `.env` y editalo con tus valores reales.
    - **IMPORTANTE**: Cambia `SECRET_KEY` por una cadena larga y aleatoria.
    - Configura `DATABASE_URL` si usas una base de datos real (PostgreSQL/MySQL) en lugar de SQLite.
    - Configura las credenciales de correo si deseas envío real.

2.  **Base de Datos**:
    Si usas PostgreSQL u otra DB, asegúrate de instalar el driver (ej: `pip install psycopg2-binary`).
    El sistema creará las tablas automáticamente al iniciar, pero para producción se recomienda usar **Alembic** para migraciones (fuera del alcance de este MVP, pero recomendado a futuro).

### Ejecución
No uses `uvicorn main:app --reload` en producción. Usa **Gunicorn** con workers Uvicorn para mayor rendimiento y estabilidad en Linux/Unix.

```bash
pip install gunicorn
# Ejemplo para ejecutar con 4 workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

En Windows, puedes seguir usando `uvicorn` sin el flag `--reload`:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 2. Frontend (React/Vite)

### Construcción (Build)
No uses `npm run dev` en producción. Debes compilar el código estático.

1.  Asegúrate de que la URL del backend sea correcta en `src/api.js`.
    *Tip: Puedes usar variables de entorno de Vite (`VITE_API_URL`) para esto.*

2.  Ejecuta el comando de construcción:
    ```bash
    npm run build
    ```
    Esto creará una carpeta `dist/` con archivos HTML/CSS/JS optimizados.

### Servir el Frontend
Sirve el contenido de la carpeta `dist/` usando un servidor web de alto redimiento como **Nginx**, **Apache** o servicios de hosting como **Vercel**, **Netlify**, o **AWS S3**.

Ejemplo simple de configuración Nginx:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        root /ruta/al/proyecto/frontend/dist;
        try_files $uri $uri/ /index.html;  # Importante para SPA (Single Page Application)
    }
}
```

## 3. Seguridad
- **HTTPS**: Asegúrate de servir tanto el Frontend como el Backend sobre HTTPS usando certificados SSL (Let's Encrypt es gratuito).
- **CORS**: En `backend/.env`, configura `ALLOWED_ORIGINS` para permitir solo tu dominio de frontend, no `*` ni `localhost`.
