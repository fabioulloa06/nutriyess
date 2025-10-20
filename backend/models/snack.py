from sqlalchemy import Column, Integer, String, Float, Text, Enum, Boolean
from database import Base
import enum

class SnackCategory(str, enum.Enum):
    SWEET = "dulce"
    SALTY = "salado"
    PROTEIN = "proteina"
    FRUIT = "fruta"
    VEGETABLE = "vegetal"
    MIXED = "mixto"

class Snack(Base):
    __tablename__ = "snacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(SnackCategory))
    description = Column(Text)
    recipe = Column(Text)
    
    # Nutritional information
    calories = Column(Float)
    proteins = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)
    
    # Dietary flags
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_diabetic_friendly = Column(Boolean, default=False)
    is_low_sodium = Column(Boolean, default=False)
    
    # Custom flag
    is_custom = Column(Boolean, default=False)


