from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NutriYess API",
    description="API para gestión nutricional de pacientes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes temporalmente
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenido a NutriYess API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Importar rutas solo después de que la app esté creada
try:
    from api.routes import auth
    app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
    logger.info("Auth router loaded successfully")
except Exception as e:
    logger.error(f"Error loading auth router: {e}")

try:
    from api.routes import patients_auth
    app.include_router(patients_auth.router, prefix="/api/patients", tags=["Pacientes"])
    logger.info("Patients router loaded successfully")
except Exception as e:
    logger.error(f"Error loading patients router: {e}")

try:
    from api.routes import menus
    app.include_router(menus.router, prefix="/api/menus", tags=["Menús"])
    logger.info("Menus router loaded successfully")
except Exception as e:
    logger.error(f"Error loading menus router: {e}")

try:
    from api.routes import meal_plans
    app.include_router(meal_plans.router, prefix="/api/meal-plans", tags=["Planes Alimenticios"])
    logger.info("Meal plans router loaded successfully")
except Exception as e:
    logger.error(f"Error loading meal plans router: {e}")

try:
    from api.routes import consultations
    app.include_router(consultations.router, prefix="/api/consultations", tags=["Consultas"])
    logger.info("Consultations router loaded successfully")
except Exception as e:
    logger.error(f"Error loading consultations router: {e}")

try:
    from api.routes import food_exchanges
    app.include_router(food_exchanges.router, prefix="/api/food-exchanges", tags=["Intercambios"])
    logger.info("Food exchanges router loaded successfully")
except Exception as e:
    logger.error(f"Error loading food exchanges router: {e}")

try:
    from api.routes import snacks
    app.include_router(snacks.router, prefix="/api/snacks", tags=["Snacks"])
    logger.info("Snacks router loaded successfully")
except Exception as e:
    logger.error(f"Error loading snacks router: {e}")

try:
    from api.routes import preferences
    app.include_router(preferences.router, prefix="/api/preferences", tags=["Preferencias"])
    logger.info("Preferences router loaded successfully")
except Exception as e:
    logger.error(f"Error loading preferences router: {e}")

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        logger.info("Creating database tables...")
        from database import engine, Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # Don't fail startup if database creation fails


