# NutriYess Backend

API REST construida con FastAPI para el sistema de gestión nutricional NutriYess.

## Estructura del Proyecto

```
backend/
├── main.py                 # Punto de entrada de la aplicación
├── database.py             # Configuración de la base de datos
├── requirements.txt        # Dependencias de Python
├── models/                 # Modelos de SQLAlchemy
│   ├── __init__.py
│   ├── patient.py          # Modelo de paciente
│   ├── menu.py             # Modelo de menú
│   ├── meal_plan.py        # Modelo de plan alimenticio
│   ├── consultation.py     # Modelo de consulta
│   ├── food_exchange.py    # Modelo de intercambio alimenticio
│   └── snack.py            # Modelo de snack
├── api/                    # Rutas de la API
│   └── routes/
│       ├── patients.py     # Endpoints de pacientes
│       ├── menus.py        # Endpoints de menús
│       ├── meal_plans.py   # Endpoints de planes alimenticios
│       ├── consultations.py # Endpoints de consultas
│       ├── food_exchanges.py # Endpoints de intercambios
│       └── snacks.py       # Endpoints de snacks
└── utils/                  # Utilidades
    └── nutrition_calculations.py # Cálculos nutricionales
```

## Modelos de Base de Datos

### Patient (Paciente)
- Información personal y demográfica
- Datos antropométricos (peso, altura)
- Historia clínica y nutricional
- Tipo de paciente y nivel de actividad
- Condiciones médicas

### Menu (Menú)
- Menús predefinidos por categoría
- Información nutricional completa
- Distribución por tiempos de comida
- Suplementos (para deportistas)

### MealPlan (Plan Alimenticio)
- Planes personalizados por paciente
- Cálculo automático de totales nutricionales
- Items individuales con porciones

### Consultation (Consulta)
- Registro de consultas médicas
- Mediciones antropométricas
- Cálculos nutricionales del momento
- Notas y recomendaciones
- Programación de próximas citas

### FoodExchange (Intercambio Alimenticio)
- Lista de alimentos por categoría
- Información de porciones
- Valores nutricionales por porción

### Snack (Snack)
- Recetas de snacks saludables
- Información nutricional
- Filtros dietéticos (vegetariano, vegano, etc.)

## Cálculos Nutricionales

### IMC (Índice de Masa Corporal)
```python
IMC = peso(kg) / (altura(m))²
```

Categorías según edad:
- Niños/Adolescentes: Percentiles
- Adultos: Bajo peso (<18.5), Normal (18.5-24.9), Sobrepeso (25-29.9), Obesidad (≥30)
- Adultos mayores: Rangos ajustados

### Peso Ideal (Fórmula de Devine)
```python
Hombres: 50 kg + 2.3 kg por pulgada sobre 5 pies
Mujeres: 45.5 kg + 2.3 kg por pulgada sobre 5 pies
```

### Peso Ajustado
```python
Peso ajustado = Peso ideal + 0.25 * (Peso actual - Peso ideal)
```
Usado cuando hay obesidad para cálculos nutricionales.

### TMB (Tasa Metabólica Basal)
Ecuación de Harris-Benedict revisada:

**Hombres:**
```python
TMB = 88.362 + (13.397 × peso) + (4.799 × altura) - (5.677 × edad)
```

**Mujeres:**
```python
TMB = 447.593 + (9.247 × peso) + (3.098 × altura) - (4.330 × edad)
```

### Requerimiento Calórico Total
```python
Calorías = TMB × Factor de Actividad × Factor de Estrés
```

**Factores de Actividad:**
- Sedentario: 1.2
- Ligero: 1.375
- Moderado: 1.55
- Activo: 1.725
- Muy Activo: 1.9

**Factores de Estrés por Tipo de Paciente:**
- Sano: 1.0
- Hospitalizado: 1.2
- UCI: 1.5
- Deportista: 1.3
- Adolescente: 1.15
- Adulto Mayor: 1.0
- Embarazada: 1.15 + 300 kcal

### Distribución de Macronutrientes

**Proteínas:**
- General: 1.0 g/kg
- Deportista: 1.8 g/kg
- Adulto Mayor: 1.2 g/kg

**Grasas:** 25-30% de calorías totales

**Carbohidratos:** Resto de calorías

## API Endpoints

### Health Check
```
GET / - Mensaje de bienvenida
GET /health - Estado del servidor
```

### Pacientes

```
GET    /api/patients           - Listar pacientes (paginado)
POST   /api/patients           - Crear paciente
GET    /api/patients/{id}      - Obtener paciente específico
PUT    /api/patients/{id}      - Actualizar paciente
DELETE /api/patients/{id}      - Eliminar paciente
GET    /api/patients/{id}/calculations - Obtener cálculos nutricionales
GET    /api/patients/search/{query} - Buscar pacientes
```

### Menús

```
GET    /api/menus              - Listar menús (filtro opcional por categoría)
POST   /api/menus              - Crear menú
GET    /api/menus/{id}         - Obtener menú específico
PUT    /api/menus/{id}         - Actualizar menú
DELETE /api/menus/{id}         - Eliminar menú
POST   /api/menus/seed-default-menus - Cargar menús predefinidos
```

### Planes Alimenticios

```
GET    /api/meal-plans/patient/{patient_id} - Planes de un paciente
GET    /api/meal-plans/{id}    - Obtener plan específico
POST   /api/meal-plans         - Crear plan
PUT    /api/meal-plans/{id}    - Actualizar plan
DELETE /api/meal-plans/{id}    - Eliminar plan
```

### Consultas

```
GET    /api/consultations/patient/{patient_id} - Consultas de un paciente
GET    /api/consultations/{id} - Obtener consulta específica
POST   /api/consultations      - Crear consulta
PUT    /api/consultations/{id} - Actualizar consulta
DELETE /api/consultations/{id} - Eliminar consulta
GET    /api/consultations/upcoming/all - Próximas citas
```

### Intercambios Alimenticios

```
GET    /api/food-exchanges     - Listar intercambios
POST   /api/food-exchanges     - Crear intercambio
GET    /api/food-exchanges/{id} - Obtener intercambio
PUT    /api/food-exchanges/{id} - Actualizar intercambio
DELETE /api/food-exchanges/{id} - Eliminar intercambio
POST   /api/food-exchanges/seed-default-exchanges - Cargar lista predefinida
```

### Snacks

```
GET    /api/snacks             - Listar snacks (con filtros opcionales)
POST   /api/snacks             - Crear snack
GET    /api/snacks/{id}        - Obtener snack
PUT    /api/snacks/{id}        - Actualizar snack
DELETE /api/snacks/{id}        - Eliminar snack
POST   /api/snacks/seed-default-snacks - Cargar snacks predefinidos
```

## Configuración

### Variables de Entorno

```bash
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nutriyess
```

### CORS

El backend está configurado para aceptar peticiones desde:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

## Ejecutar el Servidor

```bash
# Modo desarrollo (con recarga automática)
uvicorn main:app --reload --port 8000

# Modo producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Documentación Interactiva

FastAPI genera automáticamente documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Migraciones de Base de Datos

El proyecto usa SQLAlchemy. Las tablas se crean automáticamente al iniciar la aplicación.

Para producción, se recomienda usar Alembic para migraciones:

```bash
# Inicializar Alembic
alembic init alembic

# Crear migración
alembic revision --autogenerate -m "descripción"

# Aplicar migración
alembic upgrade head
```

## Testing

Agregar tests usando pytest:

```bash
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

## Deployment

### Docker

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Railway / Heroku

Crear `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Optimizaciones Futuras

- [ ] Autenticación JWT
- [ ] Cache con Redis
- [ ] Paginación mejorada
- [ ] Rate limiting
- [ ] Logging avanzado
- [ ] Tests unitarios y de integración
- [ ] CI/CD pipeline


