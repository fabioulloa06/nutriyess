# Dockerfile para NutriYess Backend (Railway)
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY backend/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY backend/ .

# Exponer el puerto (Railway usará su propio $PORT)
EXPOSE 8000

# Comando de inicio — usa el puerto asignado por Railway
CMD ["bash", "-c", "uvicorn main_simple:app --host 0.0.0.0 --port ${PORT:-8000}"]
