from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from database import get_db
from models.patient import Patient, Gender, ActivityLevel, PatientType
from models.user import User
from pydantic import BaseModel
from utils.nutrition_calculations import (
    calculate_bmi,
    calculate_ideal_weight,
    calculate_adjusted_weight,
    calculate_caloric_requirement,
    get_bmi_category,
    calculate_age
)
from utils.auth import get_current_user, check_subscription_status, get_patient_limit

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
    
    # Contact information
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    
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
    nutritionist_id: int
    first_name: str
    last_name: str
    identification: str
    birth_date: date
    gender: Gender
    weight: float
    height: float
    
    # Contact information
    email: str | None
    phone: str | None
    address: str | None
    
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
    age: int

# Endpoints
@router.get("/", response_model=List[PatientResponse])
def get_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all patients for the current nutritionist."""
    # Check subscription status
    is_active, message = check_subscription_status(current_user)
    if not is_active:
        raise HTTPException(
            status_code=402,
            detail=f"Subscription required: {message}"
        )
    
    patients = db.query(Patient).filter(Patient.nutritionist_id == current_user.id).all()
    return patients

@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new patient."""
    # Check subscription status
    is_active, message = check_subscription_status(current_user)
    if not is_active:
        raise HTTPException(
            status_code=402,
            detail=f"Subscription required: {message}"
        )
    
    # Check patient limit
    current_patients = db.query(Patient).filter(Patient.nutritionist_id == current_user.id).count()
    patient_limit = get_patient_limit(current_user)
    
    if patient_limit != -1 and current_patients >= patient_limit:
        raise HTTPException(
            status_code=402,
            detail=f"Patient limit reached ({patient_limit}). Upgrade your subscription to add more patients."
        )
    
    # Check if identification already exists for this nutritionist
    existing_patient = db.query(Patient).filter(
        Patient.nutritionist_id == current_user.id,
        Patient.identification == patient.identification
    ).first()
    
    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="Patient with this identification already exists"
        )
    
    db_patient = Patient(
        **patient.model_dump(),
        nutritionist_id=current_user.id
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific patient."""
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.nutritionist_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a patient."""
    db_patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.nutritionist_id == current_user.id
    ).first()
    
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a patient."""
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.nutritionist_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

@router.get("/{patient_id}/calculations", response_model=PatientCalculations)
def get_patient_calculations(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get nutritional calculations for a patient."""
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.nutritionist_id == current_user.id
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Calculate values
    bmi = calculate_bmi(patient.weight, patient.height)
    bmi_category = get_bmi_category(bmi)
    ideal_weight = calculate_ideal_weight(patient.gender, patient.height)
    adjusted_weight = calculate_adjusted_weight(patient.weight, ideal_weight)
    age = calculate_age(patient.birth_date)
    caloric_requirement = calculate_caloric_requirement(
        gender=patient.gender,
        weight=patient.weight,
        height=patient.height,
        age=age,
        activity_level=patient.activity_level,
        patient_type=patient.patient_type
    )
    
    return PatientCalculations(
        bmi=bmi,
        bmi_category=bmi_category,
        ideal_weight=ideal_weight,
        adjusted_weight=adjusted_weight,
        caloric_requirement=caloric_requirement,
        age=age
    )

@router.get("/search/{query}")
def search_patients(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search patients by name or identification."""
    patients = db.query(Patient).filter(
        Patient.nutritionist_id == current_user.id,
        (Patient.first_name.contains(query) | 
         Patient.last_name.contains(query) | 
         Patient.identification.contains(query))
    ).all()
    
    return patients
