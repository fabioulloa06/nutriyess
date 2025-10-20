@echo off
echo 🚀 NutriYess - Iniciando con Docker Compose
echo ==========================================

echo 📦 Construyendo contenedores...
docker-compose build

echo 🌐 Iniciando servicios...
docker-compose up -d

echo ⏳ Esperando que los servicios estén listos...
timeout /t 10 /nobreak

echo 📋 Estado de los servicios:
docker-compose ps

echo.
echo ✅ NutriYess está ejecutándose:
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo 📊 Base de datos: localhost:5432
echo.
echo 📝 Para ver logs: docker-compose logs -f
echo 🛑 Para detener: docker-compose down
echo.

pause
