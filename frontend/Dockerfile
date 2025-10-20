# Dockerfile para Frontend NutriYess
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY frontend/package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY frontend/ .

# Exponer puerto
EXPOSE 3000

# Comando de inicio
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]