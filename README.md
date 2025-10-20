# 🥗 NutriYess - Sistema de Gestión Nutricional

![NutriYess Logo](https://img.shields.io/badge/NutriYess-Nutrition%20Management-green?style=for-the-badge&logo=health)

**NutriYess** es una aplicación web profesional para la gestión nutricional de pacientes, diseñada específicamente para nutricionistas y profesionales de la salud en Colombia.

## ✨ Características Principales

### 👥 Gestión de Pacientes
- **Registro completo** con datos antropométricos detallados
- **Historia clínica** y nutricional
- **Seguimiento** de consultas y evolución
- **Cálculos automáticos** de IMC, peso ideal y requerimientos calóricos

### 📊 Datos Antropométricos Completos
- Medidas básicas (peso, altura, % grasa corporal)
- Circunferencias (cintura, cadera, brazo, muslo, pantorrilla)
- Pliegues cutáneos (tríceps, bíceps, subescapular, suprailiaco, abdominal)
- Masa muscular y composición corporal

### 🍽️ Planificación Alimentaria
- **Menús especializados** por condición de salud
- **Lista de intercambios** con alimentos colombianos
- **Planes alimenticios** personalizados
- **Cálculo automático** de calorías por día

### 🎯 Condiciones Especiales
- Diabetes
- Hipertensión
- Distensión abdominal
- Dietas vegetarianas y veganas
- Deportistas con suplementos

### 🇨🇴 Alimentos Colombianos
- Base de datos completa de alimentos típicos
- Arepas, pandebono, almojábana, buñuelos
- Frutas tropicales (guanábana, lulo, gulupa, granadilla)
- Verduras y legumbres locales

## 🚀 Tecnologías

### Backend
- **Python 3.11+** con FastAPI
- **PostgreSQL** para producción
- **SQLAlchemy** ORM
- **Pydantic** para validación de datos

### Frontend
- **React 18** con Vite
- **TailwindCSS** para estilos
- **Axios** para comunicación con API
- **Lucide React** para iconos

### Despliegue
- **Railway** para backend (gratuito)
- **Vercel** para frontend (gratuito)
- **PostgreSQL** incluido
- **SSL** automático

## 📦 Instalación Local

### Prerrequisitos
- Python 3.11+
- Node.js 18+
- Git

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Despliegue en la Nube (Gratuito)

### Opción 1: Railway + Vercel (Recomendada)
1. **Railway** (Backend): [railway.app](https://railway.app)
2. **Vercel** (Frontend): [vercel.com](https://vercel.com)
3. **Costo:** $0/mes

### Opción 2: Supabase + Vercel
1. **Supabase** (Base de datos): [supabase.com](https://supabase.com)
2. **Vercel** (Frontend + Backend): [vercel.com](https://vercel.com)
3. **Costo:** $0/mes

## 📋 Guías de Despliegue

- [Guía Completa de Despliegue](DEPLOYMENT_GUIDE.md)
- [Despliegue Rápido](QUICK_DEPLOY.md)
- [Configuración Local](QUICK_START.md)

## 🎯 Casos de Uso

### Para Nutricionistas
- Gestión completa de pacientes
- Seguimiento de evolución nutricional
- Planificación de menús personalizados
- Reportes y estadísticas

### Para Clínicas
- Múltiples profesionales
- Base de datos centralizada
- Reportes institucionales
- Integración con sistemas existentes

### Para Consultorios Médicos
- Evaluación nutricional rápida
- Recomendaciones automáticas
- Seguimiento de pacientes crónicos
- Integración con historia clínica

## 💰 Modelo de Comercialización

### Trial Gratuito: 30 días
- Hasta 3 pacientes
- Todas las funciones
- Sin compromiso

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

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Contacto

- **Desarrollador:** Fabio
- **Email:** tu-email@ejemplo.com
- **LinkedIn:** [Tu LinkedIn](https://linkedin.com/in/tu-perfil)

## 🙏 Agradecimientos

- Comunidad de desarrolladores Python
- Comunidad React
- Profesionales de la nutrición en Colombia
- Contribuidores de código abierto

---

**¡NutriYess - Tu aliado en la gestión nutricional profesional!** 🥗✨