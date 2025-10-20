from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.patient_preferences import PatientPreferences
from models.patient import Patient
from pydantic import BaseModel

router = APIRouter()

# Schemas
class PreferencesCreate(BaseModel):
    patient_id: int
    favorite_foods: str | None = None
    disliked_foods: str | None = None
    allergies: str | None = None
    preferred_cooking_methods: str | None = None
    cultural_restrictions: str | None = None
    budget_level: str | None = "medio"
    cooking_time_available: str | None = "medio"
    likes_sweet: int = 3
    likes_salty: int = 3
    likes_spicy: int = 3
    likes_sour: int = 3
    likes_bitter: int = 3
    prefers_soft_textures: bool = True
    prefers_crunchy_textures: bool = True
    breakfast_time: str | None = None
    lunch_time: str | None = None
    dinner_time: str | None = None
    snacks_per_day: int = 2
    additional_notes: str | None = None

class PreferencesUpdate(BaseModel):
    favorite_foods: str | None = None
    disliked_foods: str | None = None
    allergies: str | None = None
    preferred_cooking_methods: str | None = None
    cultural_restrictions: str | None = None
    budget_level: str | None = None
    cooking_time_available: str | None = None
    likes_sweet: int | None = None
    likes_salty: int | None = None
    likes_spicy: int | None = None
    likes_sour: int | None = None
    likes_bitter: int | None = None
    prefers_soft_textures: bool | None = None
    prefers_crunchy_textures: bool | None = None
    breakfast_time: str | None = None
    lunch_time: str | None = None
    dinner_time: str | None = None
    snacks_per_day: int | None = None
    additional_notes: str | None = None

class PreferencesResponse(BaseModel):
    id: int
    patient_id: int
    favorite_foods: str | None
    disliked_foods: str | None
    allergies: str | None
    preferred_cooking_methods: str | None
    cultural_restrictions: str | None
    budget_level: str | None
    cooking_time_available: str | None
    likes_sweet: int
    likes_salty: int
    likes_spicy: int
    likes_sour: int
    likes_bitter: int
    prefers_soft_textures: bool
    prefers_crunchy_textures: bool
    breakfast_time: str | None
    lunch_time: str | None
    dinner_time: str | None
    snacks_per_day: int
    additional_notes: str | None

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=PreferencesResponse)
def create_preferences(preferences: PreferencesCreate, db: Session = Depends(get_db)):
    """Crear preferencias para un paciente"""
    
    # Verificar que el paciente existe
    patient = db.query(Patient).filter(Patient.id == preferences.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar si ya tiene preferencias
    existing = db.query(PatientPreferences)\
        .filter(PatientPreferences.patient_id == preferences.patient_id)\
        .first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Este paciente ya tiene preferencias. Usa PUT para actualizar."
        )
    
    # Crear preferencias
    new_preferences = PatientPreferences(**preferences.dict())
    
    db.add(new_preferences)
    db.commit()
    db.refresh(new_preferences)
    
    return new_preferences

@router.get("/patient/{patient_id}", response_model=PreferencesResponse)
def get_patient_preferences(patient_id: int, db: Session = Depends(get_db)):
    """Obtener preferencias de un paciente"""
    preferences = db.query(PatientPreferences)\
        .filter(PatientPreferences.patient_id == patient_id)\
        .first()
    
    if not preferences:
        raise HTTPException(status_code=404, detail="Preferencias no encontradas")
    
    return preferences

@router.put("/patient/{patient_id}", response_model=PreferencesResponse)
def update_preferences(
    patient_id: int,
    preferences_data: PreferencesUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar preferencias de un paciente"""
    preferences = db.query(PatientPreferences)\
        .filter(PatientPreferences.patient_id == patient_id)\
        .first()
    
    if not preferences:
        raise HTTPException(status_code=404, detail="Preferencias no encontradas")
    
    # Actualizar campos
    for field, value in preferences_data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(preferences, field, value)
    
    db.commit()
    db.refresh(preferences)
    
    return preferences

@router.delete("/patient/{patient_id}")
def delete_preferences(patient_id: int, db: Session = Depends(get_db)):
    """Eliminar preferencias de un paciente"""
    preferences = db.query(PatientPreferences)\
        .filter(PatientPreferences.patient_id == patient_id)\
        .first()
    
    if not preferences:
        raise HTTPException(status_code=404, detail="Preferencias no encontradas")
    
    db.delete(preferences)
    db.commit()
    
    return {"message": "Preferencias eliminadas exitosamente"}

@router.get("/patient/{patient_id}/recommendations")
def get_recommendations(patient_id: int, db: Session = Depends(get_db)):
    """Obtener recomendaciones basadas en preferencias del paciente"""
    
    # Obtener paciente
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Obtener preferencias
    preferences = db.query(PatientPreferences)\
        .filter(PatientPreferences.patient_id == patient_id)\
        .first()
    
    if not preferences:
        return {
            "message": "No hay preferencias registradas para este paciente",
            "recommendations": []
        }
    
    # Generar recomendaciones basadas en preferencias
    recommendations = []
    
    # Recomendaciones por presupuesto
    if preferences.budget_level == "bajo":
        recommendations.append({
            "category": "Presupuesto",
            "title": "Alimentos económicos y nutritivos",
            "items": [
                "Fríjoles y lentejas (proteína económica)",
                "Huevos (alta calidad proteica)",
                "Avena (carbohidrato saludable)",
                "Plátano verde (versátil y económico)",
                "Zanahoria y ahuyama (vitaminas económicas)"
            ]
        })
    
    # Recomendaciones por tiempo de cocina
    if preferences.cooking_time_available == "poco":
        recommendations.append({
            "category": "Tiempo de Preparación",
            "title": "Opciones rápidas (<15 min)",
            "items": [
                "Huevos revueltos con vegetales",
                "Ensalada de atún con aguacate",
                "Smoothie de frutas con avena",
                "Arepa con queso y aguacate",
                "Yogurt con frutas y granola"
            ]
        })
    
    # Recomendaciones por preferencias de sabor
    if preferences.likes_sweet >= 4:
        recommendations.append({
            "category": "Sabores Dulces",
            "title": "Opciones saludables dulces",
            "items": [
                "Batido de guanábana",
                "Bocadillo con queso",
                "Frutas: mango, papaya, piña",
                "Avena con panela y canela",
                "Smoothie de gulupa y plátano"
            ]
        })
    
    if preferences.likes_salty >= 4:
        recommendations.append({
            "category": "Sabores Salados",
            "title": "Snacks salados saludables",
            "items": [
                "Maní tostado sin sal agregada",
                "Queso campesino",
                "Palitos de zanahoria con hummus",
                "Patacones al horno",
                "Chicharrón de cerdo (moderado)"
            ]
        })
    
    # Recomendaciones por método de cocción preferido
    if preferences.preferred_cooking_methods and "hervido" in preferences.preferred_cooking_methods.lower():
        recommendations.append({
            "category": "Métodos de Cocción",
            "title": "Recetas hervidas saludables",
            "items": [
                "Sancocho de pollo con vegetales",
                "Sudado de pescado",
                "Mazamorra de maíz",
                "Ajiaco santafereño",
                "Caldo de costilla con papa criolla"
            ]
        })
    
    # Recomendaciones por alergias (evitar)
    if preferences.allergies:
        recommendations.append({
            "category": "Alergias",
            "title": f"Evitar: {preferences.allergies}",
            "items": [
                "Revisa siempre las etiquetas",
                "Consulta con tu nutricionista alternativas",
                "Informa en restaurantes sobre tus alergias"
            ]
        })
    
    # Recomendaciones por condiciones médicas del paciente
    if patient.has_diabetes:
        recommendations.append({
            "category": "Diabetes",
            "title": "Alimentos recomendados",
            "items": [
                "Cereales integrales (bajo índice glucémico)",
                "Aguacate (grasas saludables)",
                "Proteínas magras (pescado, pollo)",
                "Vegetales no almidonados",
                "Controlar porciones de frutas"
            ]
        })
    
    if patient.has_hypertension:
        recommendations.append({
            "category": "Hipertensión",
            "title": "Alimentos bajos en sodio",
            "items": [
                "Frutas frescas (potasio natural)",
                "Vegetales sin sal agregada",
                "Hierbas aromáticas en lugar de sal",
                "Pescado al horno o vapor",
                "Evitar quesos costeños (altos en sodio)"
            ]
        })
    
    return {
        "patient_name": patient.name,
        "preferences_configured": True,
        "recommendations": recommendations
    }

