@echo off
echo 🚀 NutriYess - Creando Usuario Administrador
echo ==========================================

cd backend

echo 📦 Instalando dependencias...
pip install -r requirements.txt

echo 🔐 Ejecutando script de creación de administrador...
python create_admin.py

pause
