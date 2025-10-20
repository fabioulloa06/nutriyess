@echo off
echo ========================================
echo    Iniciando NutriYess Backend
echo ========================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
echo Entorno virtual activado
echo.

echo Iniciando servidor FastAPI en http://localhost:8000
echo Documentacion API: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python -m uvicorn main:app --reload --port 8000

pause


