# ==============================
# Dockerfile para NutriYess Backend - Compatible con Railway
# ==============================

# Imagen base ligera de Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias (gcc, cliente PostgreSQL, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias primero para aprovechar la caché de Docker
COPY backend/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente del backend
COPY backend/ .

# Exponer el puerto por defecto (8000) para desarrollo local
EXPOSE 8000

# Comando de inicio
# Usa el puerto dinámico que Railway asigna mediante la variable de entorno $PORT.
# Si no existe (modo local), usa el puerto 8000.
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

