# NutriYess - Guía de Despliegue Gratuito

## 🚀 DESPLIEGUE GRATUITO EN LA NUBE

### 📋 REQUISITOS PREVIOS
- Cuenta en GitHub (gratuita)
- Cuenta en Railway (gratuita)
- Cuenta en Vercel (gratuita)

---

## 🚂 PASO 1: CONFIGURAR RAILWAY (BACKEND)

### 1.1 Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Regístrate con GitHub
3. Conecta tu repositorio

### 1.2 Configurar el proyecto
1. Clic en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Elige tu repositorio NutriYess
4. Railway detectará automáticamente el backend

### 1.3 Configurar base de datos
1. En Railway, clic en "New" → "Database" → "PostgreSQL"
2. Railway creará automáticamente la variable `DATABASE_URL`
3. Tu backend se conectará automáticamente

### 1.4 Variables de entorno en Railway
```
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura
ALLOWED_ORIGINS=https://nutriyess.vercel.app
```

---

## ⚡ PASO 2: CONFIGURAR VERCEL (FRONTEND)

### 2.1 Crear cuenta en Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Regístrate con GitHub
3. Conecta tu repositorio

### 2.2 Configurar el proyecto
1. Clic en "New Project"
2. Selecciona tu repositorio NutriYess
3. Configura:
   - **Framework Preset:** Vite
   - **Root Directory:** frontend
   - **Build Command:** npm run build
   - **Output Directory:** dist

### 2.3 Variables de entorno en Vercel
```
VITE_API_URL=https://tu-proyecto.up.railway.app/api
```

---

## 🔧 PASO 3: CONFIGURAR LA APLICACIÓN

### 3.1 Actualizar configuración del backend
El archivo `backend/database.py` ya está configurado para usar PostgreSQL en producción.

### 3.2 Actualizar configuración del frontend
El archivo `frontend/src/api/axios.js` ya está configurado para usar variables de entorno.

---

## 🌐 PASO 4: CONFIGURAR DOMINIO PERSONALIZADO (OPCIONAL)

### 4.1 Dominio gratuito
- Usa el dominio de Railway: `tu-proyecto.up.railway.app`
- Usa el dominio de Vercel: `tu-proyecto.vercel.app`

### 4.2 Dominio personalizado (cuando tengas ingresos)
1. Compra un dominio (ej: nutriyess.com)
2. Configura DNS en Railway y Vercel
3. SSL automático incluido

---

## 📊 MONITOREO Y ESCALAMIENTO

### Límites gratuitos:
- **Railway:** 500 horas/mes (suficiente para empezar)
- **Vercel:** 100GB bandwidth/mes
- **PostgreSQL:** 1GB de almacenamiento

### Cuando necesites escalar:
- **Railway Pro:** $5/mes (más horas y recursos)
- **Vercel Pro:** $20/mes (más bandwidth y funciones)
- **PostgreSQL:** $5/mes (más almacenamiento)

---

## 🎯 ESTRATEGIA DE COMERCIALIZACIÓN

### Fase 1: MVP Gratuito (0-3 meses)
- Usa servicios gratuitos
- Enfócate en conseguir primeros clientes
- Valida el producto en el mercado

### Fase 2: Crecimiento (3-6 meses)
- Actualiza a planes básicos ($10-20/mes)
- Implementa características premium
- Establece precios de suscripción

### Fase 3: Escalamiento (6+ meses)
- Migra a AWS/Azure para mayor control
- Implementa características empresariales
- Expande a múltiples países

---

## 💰 MODELO DE PRECIOS SUGERIDO

### Plan Básico: $29/mes
- Hasta 50 pacientes
- Funciones básicas
- Soporte por email

### Plan Profesional: $79/mes
- Hasta 200 pacientes
- Todas las funciones
- Soporte prioritario
- Reportes avanzados

### Plan Empresarial: $199/mes
- Pacientes ilimitados
- API personalizada
- Integraciones
- Soporte dedicado

---

## 🚀 PRÓXIMOS PASOS

1. **Hoy:** Configura Railway y Vercel
2. **Esta semana:** Prueba el despliegue
3. **Próximo mes:** Consigue primeros clientes beta
4. **3 meses:** Lanza comercialmente

¡Tu aplicación estará lista para comercializar en menos de 1 hora!
