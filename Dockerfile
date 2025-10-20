# Dockerfile para NutriYess Backend - Versión Simple
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para mejor cache)
COPY backend/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY backend/ .

# Exponer puerto
EXPOSE 8000

# Comando de inicio - versión simple que funciona
CMD ["python", "-m", "uvicorn", "main_simple:app", "--host", "0.0.0.0", "--port", "8000"]
