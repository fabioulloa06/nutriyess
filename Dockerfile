# Dockerfile para NutriYess Backend - Versión Ultra Simple
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar solo FastAPI y uvicorn
RUN pip install fastapi uvicorn

# Copiar solo el archivo de la aplicación
COPY backend/app.py .

# Exponer puerto
EXPOSE 8000

# Comando de inicio - versión ultra simple
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
