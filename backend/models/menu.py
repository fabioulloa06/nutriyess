from sqlalchemy import Column, Integer, String, Float, Text, Enum, Boolean
from database import Base
import enum

class MenuCategory(str, enum.Enum):
    HEALTHY = "sano"
    DIABETES = "diabetes"
    HYPERTENSION = "hipertension"
    BLOATING = "distension_abdominal"
    VEGETARIAN = "vegetariano"
    VEGAN = "vegano"
    ATHLETE = "deportista"
    OTHER = "otro"

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(MenuCategory), nullable=False)
    description = Column(Text)
    
    # Nutritional information
    calories = Column(Float)
    proteins = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)
    fiber = Column(Float)
    
    # Meal times
    breakfast = Column(Text)
    morning_snack = Column(Text)
    lunch = Column(Text)
    afternoon_snack = Column(Text)
    dinner = Column(Text)
    
    # Custom menu flag
    is_custom = Column(Boolean, default=False)
    
    # Supplements (for athletes)
    supplements = Column(Text)


