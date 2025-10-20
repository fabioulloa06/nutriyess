from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import patients, menus, meal_plans, consultations, food_exchanges, snacks, preferences, auth
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NutriYess API",
    description="API para gestión nutricional de pacientes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(patients.router, prefix="/api/patients", tags=["Pacientes"])
app.include_router(menus.router, prefix="/api/menus", tags=["Menús"])
app.include_router(meal_plans.router, prefix="/api/meal-plans", tags=["Planes Alimenticios"])
app.include_router(consultations.router, prefix="/api/consultations", tags=["Consultas"])
app.include_router(food_exchanges.router, prefix="/api/food-exchanges", tags=["Intercambios"])
app.include_router(snacks.router, prefix="/api/snacks", tags=["Snacks"])
app.include_router(preferences.router, prefix="/api/preferences", tags=["Preferencias"])

@app.get("/")
def root():
    return {"message": "Bienvenido a NutriYess API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


