# Etapa 1: Construcción (Build)
FROM node:18-alpine AS build

WORKDIR /app

# Copiar package.json y lockfile
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar el resto del código
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa 2: Servidor (Nginx)
FROM nginx:alpine

# Copiar los archivos construidos desde la etapa anterior
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de Nginx si es necesaria (opcional, pero recomendada para SPA)
# Crearemos un nginx.conf básico al vuelo
RUN echo 'server { \
    listen 80; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html index.htm; \
    try_files $uri $uri/ /index.html; \
    } \
    }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
