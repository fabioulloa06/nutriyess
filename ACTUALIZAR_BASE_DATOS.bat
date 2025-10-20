@echo off
title NutriYess - Actualizar Base de Datos

echo ================================================
echo    ACTUALIZANDO BASE DE DATOS - NUTRIYESS
echo ================================================
echo.
echo Este script eliminará la base de datos anterior
echo y la recreará con los nuevos cambios:
echo.
echo ✅ Micronutrientes agregados
echo ✅ Alimentos colombianos listos
echo ✅ Consultas con medidas antropométricas completas
echo ✅ Preferencias del paciente
echo ✅ Sistema de recomendaciones automáticas
echo.
pause
echo.
echo Eliminando base de datos anterior...
cd backend
del nutriyess.db 2>nul
echo Base de datos eliminada.
echo.
echo La nueva base de datos se creará automáticamente
echo cuando inicies el backend.
echo.
echo IMPORTANTE: Ahora debes:
echo 1. Cerrar el backend si está abierto (Ctrl+C)
echo 2. Ejecutar START_BACKEND.bat
echo 3. Cargar los datos desde el frontend
echo.
pause
