# 🚀 Guía Rápida de Inicio - NutriYess

Esta guía te ayudará a tener NutriYess funcionando en minutos.

## ⚡ Inicio Rápido (5 minutos)

### 1. Requisitos Previos

Asegúrate de tener instalado:
- ✅ Python 3.9+
- ✅ Node.js 16+
- ✅ PostgreSQL 13+

### 2. Configurar Base de Datos

Abre PostgreSQL y ejecuta:

```sql
CREATE DATABASE nutriyess;
```

### 3. Configurar Backend

```bash
# Navegar al directorio backend
cd backend

# Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar Frontend

Abre una **nueva terminal** y ejecuta:

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install
```

### 5. Iniciar Aplicación

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Deberías ver:
```
VITE ready in XXX ms
Local: http://localhost:3000
```

### 6. ¡Listo! 🎉

Abre tu navegador en: **http://localhost:3000**

## 📝 Primeros Pasos en la Aplicación

### 1. Cargar Datos Iniciales

Para comenzar con datos de ejemplo:

1. **Menús**: Ve a la página "Menús" → Click en "Cargar Menús Predefinidos"
2. **Intercambios**: Ve a "Intercambios" → Click en "Cargar Lista Predefinida"
3. **Snacks**: Ve a "Snacks" → Click en "Cargar Snacks Predefinidos"

### 2. Crear tu Primer Paciente

1. Ve a **"Pacientes"**
2. Click en **"Nuevo Paciente"**
3. Completa el formulario:
   - Nombres: Juan
   - Apellidos: Pérez
   - Identificación: 123456789
   - Fecha de Nacimiento: (escoge una fecha)
   - Género: Masculino
   - Peso: 75 kg
   - Altura: 175 cm
4. Click en **"Crear Paciente"**

### 3. Ver Cálculos Nutricionales

1. Click en el paciente que acabas de crear
2. Ve a la pestaña **"Cálculos"**
3. Verás automáticamente:
   - IMC
   - Peso Ideal
   - Peso Ajustado
   - TMB
   - Requerimiento Calórico
   - Distribución de Macronutrientes

### 4. Explorar Menús

1. Ve a **"Menús"**
2. Filtra por categoría (ej: "Diabetes", "Deportista")
3. Click en cualquier menú para ver detalles completos

## 🔧 Configuración Avanzada (Opcional)

### Cambiar Puerto del Backend

```bash
uvicorn main:app --reload --port 8080
```

Actualizar `frontend/vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8080',
  },
}
```

### Configurar URL de Base de Datos Personalizada

Editar `backend/database.py`:
```python
DATABASE_URL = "postgresql://usuario:contraseña@localhost:5432/nutriyess"
```

## 🐛 Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de estar en el entorno virtual
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "Connection to database failed"
- Verifica que PostgreSQL esté corriendo
- Confirma que la base de datos "nutriyess" existe
- Revisa las credenciales en `backend/database.py`

### Error: "Port 3000 already in use"
```bash
# Usa otro puerto
npm run dev -- --port 3001
```

### Error: "CORS policy"
- Verifica que el backend esté corriendo en el puerto 8000
- Revisa la configuración de CORS en `backend/main.py`

## 📚 Recursos Adicionales

- **Documentación Completa**: Ver `README.md`
- **API Docs**: http://localhost:8000/docs (con backend corriendo)
- **Backend Docs**: Ver `backend/README.md`
- **Frontend Docs**: Ver `frontend/README.md`

## 💡 Consejos

1. **Mantén ambas terminales abiertas** mientras trabajas
2. **Guarda cambios automáticamente**: Ambos servidores tienen hot-reload
3. **Usa la documentación interactiva**: http://localhost:8000/docs para probar la API
4. **Explora los menús predefinidos** antes de crear los tuyos

## ✅ Checklist de Verificación

- [ ] PostgreSQL corriendo
- [ ] Base de datos "nutriyess" creada
- [ ] Backend iniciado en puerto 8000
- [ ] Frontend iniciado en puerto 3000
- [ ] Página principal carga correctamente
- [ ] Datos predefinidos cargados
- [ ] Primer paciente creado

## 🎯 Próximos Pasos

Una vez que todo funcione:

1. Explora todas las secciones de la aplicación
2. Crea varios pacientes de prueba
3. Registra consultas
4. Crea planes alimenticios personalizados
5. Personaliza menús según tus necesidades

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa esta guía nuevamente
2. Consulta los README específicos
3. Verifica los logs en las terminales
4. Abre un issue en el repositorio

---

**¡Bienvenido a NutriYess! 🥗💚**

¡Comienza a mejorar la gestión nutricional de tus pacientes hoy mismo!


