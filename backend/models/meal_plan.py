from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date_created = Column(Date, nullable=False)
    name = Column(String)
    notes = Column(Text)
    
    total_calories = Column(Float)
    total_proteins = Column(Float)
    total_carbohydrates = Column(Float)
    total_fats = Column(Float)
    
    # Relationships
    patient = relationship("Patient", back_populates="meal_plans")
    items = relationship("MealPlanItem", back_populates="meal_plan", cascade="all, delete-orphan")

class MealPlanItem(Base):
    __tablename__ = "meal_plan_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"))
    
    meal_time = Column(String)  # Desayuno, Media mañana, Almuerzo, etc.
    food_item = Column(String)
    portion = Column(String)
    
    calories = Column(Float)
    proteins = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)
    
    # Relationships
    meal_plan = relationship("MealPlan", back_populates="items")


