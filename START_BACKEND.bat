@echo off
title NutriYess - Backend (FastAPI)

echo ================================================
echo       NUTRIYESS - BACKEND (FastAPI)
echo ================================================
echo.
echo Iniciando servidor en puerto 8000...
echo.
echo MANTÉN ESTA VENTANA ABIERTA
echo.
echo Accesos:
echo - API Docs: http://localhost:8000/docs
echo - Health: http://localhost:8000/health
echo.
echo Presiona Ctrl+C para detener
echo ================================================
echo.

cd backend
call venv\Scripts\activate.bat
echo Activando entorno virtual...
echo.
venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000

pause


