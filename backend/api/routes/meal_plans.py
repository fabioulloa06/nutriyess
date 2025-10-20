from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database import get_db
from models.meal_plan import MealPlan, MealPlanItem
from pydantic import BaseModel

router = APIRouter()

# Schemas
class MealPlanItemCreate(BaseModel):
    meal_time: str
    food_item: str
    portion: str
    calories: float
    proteins: float
    carbohydrates: float
    fats: float

class MealPlanItemResponse(BaseModel):
    id: int
    meal_plan_id: int
    meal_time: str
    food_item: str
    portion: str
    calories: float
    proteins: float
    carbohydrates: float
    fats: float

    class Config:
        from_attributes = True

class MealPlanCreate(BaseModel):
    patient_id: int
    date_created: date
    name: str | None = None
    notes: str | None = None
    items: List[MealPlanItemCreate]

class MealPlanResponse(BaseModel):
    id: int
    patient_id: int
    date_created: date
    name: str | None
    notes: str | None
    total_calories: float | None
    total_proteins: float | None
    total_carbohydrates: float | None
    total_fats: float | None
    items: List[MealPlanItemResponse]

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=MealPlanResponse)
def create_meal_plan(meal_plan: MealPlanCreate, db: Session = Depends(get_db)):
    """Crear un nuevo plan de alimentación"""
    # Calculate totals
    total_calories = sum(item.calories for item in meal_plan.items)
    total_proteins = sum(item.proteins for item in meal_plan.items)
    total_carbs = sum(item.carbohydrates for item in meal_plan.items)
    total_fats = sum(item.fats for item in meal_plan.items)
    
    # Create meal plan
    db_meal_plan = MealPlan(
        patient_id=meal_plan.patient_id,
        date_created=meal_plan.date_created,
        name=meal_plan.name,
        notes=meal_plan.notes,
        total_calories=total_calories,
        total_proteins=total_proteins,
        total_carbohydrates=total_carbs,
        total_fats=total_fats
    )
    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)
    
    # Create items
    for item in meal_plan.items:
        db_item = MealPlanItem(
            meal_plan_id=db_meal_plan.id,
            **item.model_dump()
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_meal_plan)
    return db_meal_plan

@router.get("/patient/{patient_id}", response_model=List[MealPlanResponse])
def get_patient_meal_plans(patient_id: int, db: Session = Depends(get_db)):
    """Obtener todos los planes de alimentación de un paciente"""
    meal_plans = db.query(MealPlan).filter(MealPlan.patient_id == patient_id).all()
    return meal_plans

@router.get("/{meal_plan_id}", response_model=MealPlanResponse)
def get_meal_plan(meal_plan_id: int, db: Session = Depends(get_db)):
    """Obtener un plan de alimentación específico"""
    meal_plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Plan de alimentación no encontrado")
    return meal_plan

@router.put("/{meal_plan_id}", response_model=MealPlanResponse)
def update_meal_plan(meal_plan_id: int, meal_plan_data: MealPlanCreate, db: Session = Depends(get_db)):
    """Actualizar un plan de alimentación"""
    meal_plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Plan de alimentación no encontrado")
    
    # Calculate new totals
    total_calories = sum(item.calories for item in meal_plan_data.items)
    total_proteins = sum(item.proteins for item in meal_plan_data.items)
    total_carbs = sum(item.carbohydrates for item in meal_plan_data.items)
    total_fats = sum(item.fats for item in meal_plan_data.items)
    
    # Update meal plan
    meal_plan.patient_id = meal_plan_data.patient_id
    meal_plan.date_created = meal_plan_data.date_created
    meal_plan.name = meal_plan_data.name
    meal_plan.notes = meal_plan_data.notes
    meal_plan.total_calories = total_calories
    meal_plan.total_proteins = total_proteins
    meal_plan.total_carbohydrates = total_carbs
    meal_plan.total_fats = total_fats
    
    # Delete old items
    db.query(MealPlanItem).filter(MealPlanItem.meal_plan_id == meal_plan_id).delete()
    
    # Create new items
    for item in meal_plan_data.items:
        db_item = MealPlanItem(
            meal_plan_id=meal_plan.id,
            **item.model_dump()
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(meal_plan)
    return meal_plan

@router.delete("/{meal_plan_id}")
def delete_meal_plan(meal_plan_id: int, db: Session = Depends(get_db)):
    """Eliminar un plan de alimentación"""
    meal_plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Plan de alimentación no encontrado")
    
    db.delete(meal_plan)
    db.commit()
    return {"message": "Plan de alimentación eliminado exitosamente"}


