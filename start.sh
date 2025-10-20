#!/bin/bash
# Script de inicio simple para Railway

echo "🚀 Iniciando NutriYess en Railway..."

# Instalar dependencias usando python -m pip
echo "📦 Instalando dependencias..."
python -m pip install -r requirements.txt

# Crear tablas de base de datos (solo si hay DATABASE_URL)
if [ ! -z "$DATABASE_URL" ]; then
    echo "🗄️ Creando tablas de base de datos..."
    python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
else
    echo "⚠️ No hay DATABASE_URL configurada, usando SQLite local"
fi

# Iniciar servidor usando python -m uvicorn
echo "🌐 Iniciando servidor..."
python -m uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info