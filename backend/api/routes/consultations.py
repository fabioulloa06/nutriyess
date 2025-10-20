from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.consultation import Consultation
from models.patient import Patient
from pydantic import BaseModel
from utils.nutrition_calculations import (
    calculate_bmi,
    calculate_ideal_weight,
    calculate_adjusted_weight,
    calculate_caloric_requirement,
    calculate_age
)

router = APIRouter()

# Schemas
class ConsultationCreate(BaseModel):
    patient_id: int
    consultation_date: datetime | None = None
    weight: float
    height: float
    
    # Circumferences (optional)
    waist_circumference: float | None = None
    hip_circumference: float | None = None
    arm_circumference: float | None = None
    thigh_circumference: float | None = None
    calf_circumference: float | None = None
    
    # Skinfolds (optional)
    triceps_skinfold: float | None = None
    biceps_skinfold: float | None = None
    subscapular_skinfold: float | None = None
    suprailiac_skinfold: float | None = None
    abdominal_skinfold: float | None = None
    
    # Body composition (optional)
    body_fat_percentage: float | None = None
    muscle_mass: float | None = None
    
    # Activity level changes
    activity_level_changed: int = 0  # 0=no, 1=yes
    new_activity_level: str | None = None
    
    # Notes
    notes: str | None = None
    recommendations: str | None = None
    diet_plan: str | None = None
    clinical_observations: str | None = None
    follow_up_notes: str | None = None
    next_appointment: datetime | None = None

class ConsultationResponse(BaseModel):
    id: int
    patient_id: int
    consultation_date: datetime
    weight: float
    height: float
    bmi: float | None
    weight_change: float | None
    
    # Circumferences
    waist_circumference: float | None
    hip_circumference: float | None
    arm_circumference: float | None
    thigh_circumference: float | None
    calf_circumference: float | None
    
    # Skinfolds
    triceps_skinfold: float | None
    biceps_skinfold: float | None
    subscapular_skinfold: float | None
    suprailiac_skinfold: float | None
    abdominal_skinfold: float | None
    
    # Body composition
    body_fat_percentage: float | None
    muscle_mass: float | None
    
    # Activity level
    activity_level_changed: int
    new_activity_level: str | None
    
    # Calculated values
    caloric_requirement: float | None
    healthy_weight: float | None
    adjusted_weight: float | None
    
    # Notes
    notes: str | None
    recommendations: str | None
    diet_plan: str | None
    clinical_observations: str | None
    follow_up_notes: str | None
    next_appointment: datetime | None

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=ConsultationResponse)
def create_consultation(consultation: ConsultationCreate, db: Session = Depends(get_db)):
    """Crear nueva consulta con todas las medidas antropométricas"""
    
    # Verificar que el paciente existe
    patient = db.query(Patient).filter(Patient.id == consultation.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Calcular peso anterior para el cambio
    previous_consultation = db.query(Consultation)\
        .filter(Consultation.patient_id == consultation.patient_id)\
        .order_by(Consultation.consultation_date.desc())\
        .first()
    
    weight_change = None
    if previous_consultation:
        weight_change = consultation.weight - previous_consultation.weight
    
    # Calcular BMI
    bmi = calculate_bmi(consultation.weight, consultation.height)
    
    # Calcular edad del paciente
    age = calculate_age(patient.date_of_birth)
    
    # Calcular peso saludable y ajustado
    healthy_weight = calculate_ideal_weight(consultation.height, patient.gender)
    adjusted_weight = calculate_adjusted_weight(
        consultation.weight,
        healthy_weight,
        bmi
    )
    
    # Determinar nivel de actividad
    activity_level = consultation.new_activity_level if consultation.activity_level_changed else patient.activity_level
    
    # Calcular requerimiento calórico
    caloric_requirement = calculate_caloric_requirement(
        weight=consultation.weight,
        height=consultation.height,
        age=age,
        gender=patient.gender,
        activity_level=activity_level,
        condition=patient.condition if hasattr(patient, 'condition') else "sano"
    )
    
    # Crear consulta
    new_consultation = Consultation(
        patient_id=consultation.patient_id,
        consultation_date=consultation.consultation_date or datetime.now(),
        weight=consultation.weight,
        height=consultation.height,
        bmi=bmi,
        weight_change=weight_change,
        
        # Circumferences
        waist_circumference=consultation.waist_circumference,
        hip_circumference=consultation.hip_circumference,
        arm_circumference=consultation.arm_circumference,
        thigh_circumference=consultation.thigh_circumference,
        calf_circumference=consultation.calf_circumference,
        
        # Skinfolds
        triceps_skinfold=consultation.triceps_skinfold,
        biceps_skinfold=consultation.biceps_skinfold,
        subscapular_skinfold=consultation.subscapular_skinfold,
        suprailiac_skinfold=consultation.suprailiac_skinfold,
        abdominal_skinfold=consultation.abdominal_skinfold,
        
        # Body composition
        body_fat_percentage=consultation.body_fat_percentage,
        muscle_mass=consultation.muscle_mass,
        
        # Activity level
        activity_level_changed=consultation.activity_level_changed,
        new_activity_level=consultation.new_activity_level,
        
        # Calculated values
        caloric_requirement=caloric_requirement,
        healthy_weight=healthy_weight,
        adjusted_weight=adjusted_weight,
        
        # Notes
        notes=consultation.notes,
        recommendations=consultation.recommendations,
        diet_plan=consultation.diet_plan,
        clinical_observations=consultation.clinical_observations,
        follow_up_notes=consultation.follow_up_notes,
        next_appointment=consultation.next_appointment
    )
    
    # Si cambió el nivel de actividad, actualizar el paciente
    if consultation.activity_level_changed and consultation.new_activity_level:
        patient.activity_level = consultation.new_activity_level
    
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    
    return new_consultation

@router.get("/patient/{patient_id}", response_model=List[ConsultationResponse])
def get_patient_consultations(patient_id: int, db: Session = Depends(get_db)):
    """Obtener todas las consultas de un paciente"""
    consultations = db.query(Consultation)\
        .filter(Consultation.patient_id == patient_id)\
        .order_by(Consultation.consultation_date.desc())\
        .all()
    return consultations

@router.get("/{consultation_id}", response_model=ConsultationResponse)
def get_consultation(consultation_id: int, db: Session = Depends(get_db)):
    """Obtener una consulta específica"""
    consultation = db.query(Consultation)\
        .filter(Consultation.id == consultation_id)\
        .first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    return consultation

@router.put("/{consultation_id}", response_model=ConsultationResponse)
def update_consultation(
    consultation_id: int,
    consultation_data: ConsultationCreate,
    db: Session = Depends(get_db)
):
    """Actualizar una consulta existente"""
    consultation = db.query(Consultation)\
        .filter(Consultation.id == consultation_id)\
        .first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    # Actualizar campos
    for field, value in consultation_data.dict(exclude_unset=True).items():
        setattr(consultation, field, value)
    
    # Recalcular valores si cambiaron peso o talla
    if consultation_data.weight or consultation_data.height:
        consultation.bmi = calculate_bmi(consultation.weight, consultation.height)
    
    db.commit()
    db.refresh(consultation)
    
    return consultation

@router.delete("/{consultation_id}")
def delete_consultation(consultation_id: int, db: Session = Depends(get_db)):
    """Eliminar una consulta"""
    consultation = db.query(Consultation)\
        .filter(Consultation.id == consultation_id)\
        .first()
    
    if not consultation:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    db.delete(consultation)
    db.commit()
    
    return {"message": "Consulta eliminada exitosamente"}

@router.get("/upcoming/all", response_model=List[dict])
def get_upcoming_consultations(db: Session = Depends(get_db)):
    """Obtener próximas citas programadas"""
    consultations = db.query(Consultation)\
        .filter(Consultation.next_appointment >= datetime.now())\
        .order_by(Consultation.next_appointment)\
        .all()
    
    result = []
    for consultation in consultations:
        patient = db.query(Patient).filter(Patient.id == consultation.patient_id).first()
        result.append({
            "consultation_id": consultation.id,
            "patient_id": patient.id,
            "patient_name": patient.name,
            "next_appointment": consultation.next_appointment,
            "last_weight": consultation.weight
        })
    
    return result
