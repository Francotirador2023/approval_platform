# Guía de Despliegue en Hostinger VPS (Ubuntu/Debian)

Esta guía asume que has contratado un **VPS KVM** en Hostinger con **Ubuntu 22.04** (o superior).

## Paso 1: Conectarse al Servidor (SSH)
Cuando compras el VPS, Hostinger te da una **IP Pública** y una contraseña **root**.
Abre tu terminal (PowerShell en Windows o Terminal en Mac/Linux) y escribe:

```bash
ssh root@TU_IP_DEL_VPS
# Ejemplo: ssh root@192.168.1.50
```
*Si te pregunta "Are you sure...", escribe `yes`. Introduce la contraseña (no se verá mientras escribes).*

## Paso 2: Instalar Docker y Docker Compose
Copia y pega estos comandos uno por uno en la terminal de tu VPS para instalar todo lo necesario:

```bash
# 1. Actualizar el sistema
apt update && apt upgrade -y

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Verificar instalación
docker --version
docker compose version
```

## Paso 3: Subir tu Proyecto
La forma más fácil es usando **GitHub**.

1.  **En tu computadora**: Sube tu código a un repositorio de GitHub (puede ser público o privado).
2.  **En el VPS**: Clona el repositorio.

```bash
# Si es público:
git clone https://github.com/TU_USUARIO/TU_PROYECTO.git
cd TU_PROYECTO

# Si es privado, necesitarás generar una clave SSH o usar HTTPS con token, 
# pero para empezar es más fácil hacerlo público temporalmente o usar FileZilla para subir la carpeta.
```

*Alternativa sin GitHub (usando SCP desde tu PC):*
```powershell
# Ejecuta esto DESDE TU PC (no en el VPS)
scp -r "ruta/a/tu/proyecto" root@TU_IP_DEL_VPS:/root/approval_platform
```

## Paso 4: Configurar Variables de Entorno
Dentro de la carpeta del proyecto en el VPS:

```bash
# Copiar el ejemplo
cp backend/.env.example backend/.env

# Editar el archivo con nano (editor de texto simple)
nano backend/.env
```
*   Cambia `SECRET_KEY`, pon credenciales de correo reales, etc.
*   Para guardar en Nano: `Ctrl + O`, `Enter`. Para salir: `Ctrl + X`.

## Paso 5: ¡Desplegar! 🚀
El momento de la verdad. Ejecuta:

```bash
docker compose up -d --build
```
*(El `-d` significa "detached", para que siga corriendo aunque cierres la terminal).*

## Paso 6: Verificar
Abre tu navegador y entra a: `http://TU_IP_DEL_VPS`

¡Deberías ver tu Frontend!
Tu Backend API estará en: `http://TU_IP_DEL_VPS:8000`

---

### Tips Extra:
*   **Reiniciar todo**: `docker compose restart`
*   **Ver logs**: `docker compose logs -f`
*   **Actualizar cambios**:
    1. `git pull` (descarga cambios)
    2. `docker compose up -d --build` (reconstruye)
