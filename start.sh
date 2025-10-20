#!/bin/bash
# Script de inicio para Railway

echo "🚀 Iniciando NutriYess en Railway..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Crear tablas de base de datos
echo "🗄️ Creando tablas de base de datos..."
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"

# Iniciar servidor
echo "🌐 Iniciando servidor..."
uvicorn main:app --host 0.0.0.0 --port $PORT
