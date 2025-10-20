#!/usr/bin/env python3
"""
Script de inicio robusto para Railway
"""

import os
import sys
import subprocess
import time

def main():
    print("🚀 Iniciando NutriYess en Railway...")
    
    # Verificar variables de entorno
    print("📋 Verificando configuración...")
    
    # DATABASE_URL debería estar configurada por Railway
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("⚠️ DATABASE_URL no configurada, usando SQLite local")
    else:
        print(f"✅ DATABASE_URL configurada: {database_url[:20]}...")
    
    # Instalar dependencias
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return 1
    
    # Crear tablas de base de datos
    print("🗄️ Creando tablas de base de datos...")
    try:
        from database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas")
    except Exception as e:
        print(f"⚠️ Error creando tablas: {e}")
        print("Continuando sin crear tablas...")
    
    # Iniciar servidor
    print("🌐 Iniciando servidor FastAPI...")
    port = os.getenv("PORT", "8000")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", port,
            "--log-level", "info"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error iniciando servidor: {e}")
        return 1
    except KeyboardInterrupt:
        print("🛑 Servidor detenido por el usuario")
        return 0

if __name__ == "__main__":
    sys.exit(main())
