# 🏗️ Arquitectura de NutriYess

## Visión General

NutriYess es una aplicación web full-stack para gestión nutricional con arquitectura cliente-servidor.

```
┌─────────────────────────────────────────────┐
│           FRONTEND (React + Vite)            │
│  ┌────────────────────────────────────────┐ │
│  │  React Router   │  Axios  │ TailwindCSS│ │
│  └────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST API
                   ↓
┌──────────────────────────────────────────────┐
│          BACKEND (FastAPI + Python)          │
│  ┌────────────────────────────────────────┐ │
│  │   API Routes  │  Business Logic │ Utils│ │
│  └────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────┐ │
│  │        SQLAlchemy ORM + Pydantic       │ │
│  └────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────┘
                   │ SQL
                   ↓
┌──────────────────────────────────────────────┐
│            PostgreSQL Database               │
└──────────────────────────────────────────────┘
```

## Capas de la Aplicación

### 1. Frontend (Presentación)

**Tecnologías:**
- React 18 (Componentes funcionales + Hooks)
- React Router v6 (Routing)
- TailwindCSS (Estilos)
- Axios (HTTP Client)
- Vite (Build tool)

**Estructura:**
```
src/
├── main.jsx           # Entry point
├── App.jsx            # Root component + routing
├── api/
│   └── axios.js       # API client configuration
├── components/        # Reusable components
│   └── PatientForm.jsx
└── pages/             # Page components
    ├── HomePage.jsx
    ├── PatientsPage.jsx
    ├── PatientDetailPage.jsx
    ├── MenusPage.jsx
    ├── FoodExchangesPage.jsx
    ├── SnacksPage.jsx
    └── ConsultationsPage.jsx
```

**Responsabilidades:**
- Renderizado de UI
- Gestión de estado local
- Interacción con el usuario
- Consumo de API REST

### 2. Backend (Lógica de Negocio)

**Tecnologías:**
- FastAPI (Framework web)
- SQLAlchemy (ORM)
- Pydantic (Validación)
- PostgreSQL Driver

**Estructura:**
```
backend/
├── main.py            # Application entry
├── database.py        # DB configuration
├── models/            # SQLAlchemy models
│   ├── patient.py
│   ├── menu.py
│   ├── meal_plan.py
│   ├── consultation.py
│   ├── food_exchange.py
│   └── snack.py
├── api/routes/        # API endpoints
│   ├── patients.py
│   ├── menus.py
│   ├── meal_plans.py
│   ├── consultations.py
│   ├── food_exchanges.py
│   └── snacks.py
└── utils/             # Utilities
    └── nutrition_calculations.py
```

**Responsabilidades:**
- Validación de datos
- Lógica de negocio
- Cálculos nutricionales
- Operaciones CRUD
- Gestión de base de datos

### 3. Base de Datos (Persistencia)

**Tecnología:**
- PostgreSQL 13+

**Esquema Principal:**

```sql
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Patient   │──────│ Consultation │      │  MealPlan   │
│             │ 1:N  │              │      │             │
│ - id        │      │ - id         │      │ - id        │
│ - name      │      │ - patient_id │      │ - patient_id│
│ - weight    │      │ - date       │      │ - date      │
│ - height    │      │ - bmi        │      │ - calories  │
│ - ...       │      │ - ...        │      │ - ...       │
└─────────────┘      └──────────────┘      └─────────────┘
                                                   │
                                                   │ 1:N
                                                   ↓
                                           ┌──────────────┐
                                           │ MealPlanItem │
                                           │              │
                                           │ - id         │
                                           │ - meal_time  │
                                           │ - food_item  │
                                           │ - ...        │
                                           └──────────────┘

┌──────────────┐      ┌──────────────┐      ┌─────────┐
│     Menu     │      │FoodExchange  │      │  Snack  │
│              │      │              │      │         │
│ - id         │      │ - id         │      │ - id    │
│ - name       │      │ - name       │      │ - name  │
│ - category   │      │ - category   │      │ - recipe│
│ - breakfast  │      │ - portion    │      │ - ...   │
│ - lunch      │      │ - calories   │      │         │
│ - ...        │      │ - ...        │      │         │
└──────────────┘      └──────────────┘      └─────────┘
```

## Flujo de Datos

### Crear Paciente

```
Usuario → [PatientForm] → submit()
    ↓
Validación Frontend
    ↓
POST /api/patients → [Backend]
    ↓
Validación Pydantic
    ↓
[patients.py] → create_patient()
    ↓
[SQLAlchemy] → INSERT INTO patients
    ↓
[PostgreSQL] → Guardar datos
    ↓
Response 201 Created
    ↓
Frontend actualiza UI
```

### Obtener Cálculos Nutricionales

```
Usuario → Click en paciente
    ↓
GET /api/patients/{id}/calculations
    ↓
[Backend] → get_patient_calculations()
    ↓
Obtener datos del paciente
    ↓
[nutrition_calculations.py]
    ├─ calculate_bmi()
    ├─ calculate_ideal_weight()
    ├─ calculate_adjusted_weight()
    └─ calculate_caloric_requirement()
        ├─ calculate_tmb()
        ├─ get_activity_factor()
        └─ get_stress_factor()
    ↓
Response JSON con cálculos
    ↓
Frontend muestra resultados
```

## Patrones de Diseño

### 1. Repository Pattern
SQLAlchemy actúa como capa de abstracción sobre la base de datos.

### 2. MVC (Model-View-Controller)
- **Model**: SQLAlchemy models
- **View**: React components
- **Controller**: FastAPI routes

### 3. Dependency Injection
FastAPI usa DI para gestionar dependencias como sesiones de BD:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    # ...
```

### 4. Schema Pattern
Pydantic schemas separan modelos de BD de DTOs de API:

```python
# Modelo de BD
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    # ...

# Schema de API
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    # ...
```

## Seguridad

### Actualmente Implementado
- ✅ Validación de datos con Pydantic
- ✅ CORS configurado
- ✅ SQL Injection protection (SQLAlchemy ORM)
- ✅ Type hints en Python

### Recomendado para Producción
- ⚠️ Autenticación JWT
- ⚠️ HTTPS
- ⚠️ Rate limiting
- ⚠️ Input sanitization adicional
- ⚠️ Cifrado de datos sensibles
- ⚠️ Logs de auditoría

## Escalabilidad

### Optimizaciones Actuales
- Paginación en listados
- Filtrado en servidor
- Carga diferida de relaciones

### Mejoras Futuras
```
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
   ┌───┴───┬────────┬────────┐
   ↓       ↓        ↓        ↓
[API 1] [API 2] [API 3] [API N]
   │       │        │        │
   └───────┴────┬───┴────────┘
                ↓
         ┌────────────┐
         │   Redis    │ (Cache)
         └────────────┘
                ↓
         ┌────────────┐
         │ PostgreSQL │
         └────────────┘
```

## Deployment

### Development
```
localhost:3000 (Frontend)
    ↓
localhost:8000 (Backend)
    ↓
localhost:5432 (PostgreSQL)
```

### Production (Recomendado)
```
CDN (Static Assets)
    ↓
Frontend (Vercel/Netlify)
    ↓ HTTPS
Backend (Railway/Heroku)
    ↓ SSL
PostgreSQL (Managed DB)
```

## Monitoreo y Logs

### Recomendaciones
- **Frontend**: Sentry para errores
- **Backend**: Logging con Python logging
- **Base de Datos**: pg_stat_statements
- **APM**: New Relic / DataDog

## Testing

### Estrategia de Testing

```
┌─────────────────────────────────┐
│      E2E Tests (Cypress)        │
│  Flujos completos de usuario    │
└─────────────────┬───────────────┘
                  ↓
┌─────────────────────────────────┐
│   Integration Tests (Pytest)    │
│  API endpoints + Database       │
└─────────────────┬───────────────┘
                  ↓
┌─────────────────────────────────┐
│   Unit Tests                    │
│  Frontend: Jest + RTL           │
│  Backend: Pytest                │
└─────────────────────────────────┘
```

## CI/CD Pipeline (Recomendado)

```
GitHub Push
    ↓
GitHub Actions
    ├─ Run Linter
    ├─ Run Tests
    ├─ Build Frontend
    ├─ Build Backend Docker
    └─ Run Security Scan
    ↓
Deploy to Staging
    ↓
Manual Approval
    ↓
Deploy to Production
```

## Métricas Clave

### Performance
- **TTI** (Time to Interactive): < 3s
- **API Response Time**: < 200ms (95th percentile)
- **Database Query Time**: < 50ms

### Escalabilidad
- **Concurrent Users**: 100+ (actual), 10,000+ (objetivo)
- **Requests/Second**: 50+ (actual), 1,000+ (objetivo)
- **Database Size**: < 1GB (actual), 100GB+ (soporte)

## Mantenimiento

### Backups
```
Daily: PostgreSQL dumps
Weekly: Full system backup
Monthly: Archive to cold storage
```

### Actualizaciones
```
Dependencies: Mensual
Security patches: Inmediato
Features: Sprint 2 semanas
```

## Conclusión

NutriYess utiliza una arquitectura moderna, escalable y mantenible que permite:
- ✅ Desarrollo rápido de features
- ✅ Fácil testing y debugging
- ✅ Escalabilidad horizontal
- ✅ Separación de responsabilidades
- ✅ Buena experiencia de desarrollo

---

*Última actualización: 2024*


