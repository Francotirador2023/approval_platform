# Usar imagen oficial completa de Python para asegurar herramientas de compilación
FROM python:3.11

# Establecer directorio de trabajo
WORKDIR /app

# Establecer variables de entorno para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Actualizar pip
RUN pip install --upgrade pip

# Copiar requirements (si tienes un requirements.txt, si no generamos uno al vuelo o instalamos manual)
# Para este proyecto, instalamos manual basado en lo que sabemos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Si no usas requirements.txt aun, descomenta la siguiente linea y comenta las anteriores:
# RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlmodel python-multipart python-dotenv imap-tools aiosmtplib svglib jinja2 gunicorn python-jose[cryptography] passlib[bcrypt]

# Copiar el código
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar con Gunicorn en producción
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
