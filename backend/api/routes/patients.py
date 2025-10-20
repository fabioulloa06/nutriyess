from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from database import get_db
from models.patient import Patient, Gender, ActivityLevel, PatientType
from pydantic import BaseModel
from utils.nutrition_calculations import (
    calculate_bmi,
    calculate_ideal_weight,
    calculate_adjusted_weight,
    calculate_caloric_requirement,
    get_bmi_category,
    calculate_age
)

router = APIRouter()

# Schemas
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    identification: str
    birth_date: date
    gender: Gender
    weight: float
    height: float
    
    # Additional anthropometric data (optional)
    body_fat_percentage: float | None = None
    muscle_mass: float | None = None
    waist_circumference: float | None = None
    hip_circumference: float | None = None
    arm_circumference: float | None = None
    thigh_circumference: float | None = None
    calf_circumference: float | None = None
    triceps_skinfold: float | None = None
    biceps_skinfold: float | None = None
    subscapular_skinfold: float | None = None
    suprailiac_skinfold: float | None = None
    abdominal_skinfold: float | None = None
    
    medical_history: str | None = None
    nutritional_history: str | None = None
    allergies: str | None = None
    medications: str | None = None
    patient_type: PatientType = PatientType.HEALTHY
    activity_level: ActivityLevel = ActivityLevel.MODERATE
    is_vegetarian: int = 0
    has_diabetes: int = 0
    has_hypertension: int = 0
    has_bloating: int = 0
    other_conditions: str | None = None

class PatientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    identification: str
    birth_date: date
    gender: Gender
    weight: float
    height: float
    
    # Additional anthropometric data
    body_fat_percentage: float | None
    muscle_mass: float | None
    waist_circumference: float | None
    hip_circumference: float | None
    arm_circumference: float | None
    thigh_circumference: float | None
    calf_circumference: float | None
    triceps_skinfold: float | None
    biceps_skinfold: float | None
    subscapular_skinfold: float | None
    suprailiac_skinfold: float | None
    abdominal_skinfold: float | None
    
    medical_history: str | None
    nutritional_history: str | None
    allergies: str | None
    medications: str | None
    patient_type: PatientType
    activity_level: ActivityLevel
    is_vegetarian: int
    has_diabetes: int
    has_hypertension: int
    has_bloating: int
    other_conditions: str | None

    class Config:
        from_attributes = True

class PatientCalculations(BaseModel):
    bmi: float
    bmi_category: str
    ideal_weight: float
    adjusted_weight: float
    caloric_requirement: float
    tmb: float
    proteins_g: float
    carbs_g: float
    fats_g: float

# Endpoints
@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Crear un nuevo paciente"""
    # Check if identification already exists
    existing = db.query(Patient).filter(Patient.identification == patient.identification).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un paciente con esta identificación")
    
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[PatientResponse])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de pacientes"""
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Obtener un paciente específico"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient_data: PatientCreate, db: Session = Depends(get_db)):
    """Actualizar datos de un paciente"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    for key, value in patient_data.model_dump().items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Eliminar un paciente"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    db.delete(patient)
    db.commit()
    return {"message": "Paciente eliminado exitosamente"}

@router.get("/{patient_id}/calculations", response_model=PatientCalculations)
def get_patient_calculations(patient_id: int, db: Session = Depends(get_db)):
    """Obtener cálculos nutricionales del paciente"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    age = calculate_age(patient.birth_date)
    bmi = calculate_bmi(patient.weight, patient.height)
    bmi_category = get_bmi_category(bmi, age)
    ideal_weight = calculate_ideal_weight(patient.height, patient.gender)
    adjusted_weight = calculate_adjusted_weight(patient.weight, ideal_weight)
    
    # Use adjusted weight if BMI indicates overweight/obesity
    weight_for_calc = adjusted_weight if bmi >= 25 else patient.weight
    
    calculations = calculate_caloric_requirement(
        weight=weight_for_calc,
        height=patient.height,
        age=age,
        gender=patient.gender,
        activity_level=patient.activity_level,
        patient_type=patient.patient_type
    )
    
    return {
        "bmi": bmi,
        "bmi_category": bmi_category,
        "ideal_weight": ideal_weight,
        "adjusted_weight": adjusted_weight,
        "caloric_requirement": calculations["caloric_requirement"],
        "tmb": calculations["tmb"],
        "proteins_g": calculations["proteins_g"],
        "carbs_g": calculations["carbs_g"],
        "fats_g": calculations["fats_g"]
    }

@router.get("/search/{query}")
def search_patients(query: str, db: Session = Depends(get_db)):
    """Buscar pacientes por nombre o identificación"""
    patients = db.query(Patient).filter(
        (Patient.first_name.contains(query)) |
        (Patient.last_name.contains(query)) |
        (Patient.identification.contains(query))
    ).all()
    return patients


