from sqlalchemy import Column, Integer, String, Float, Enum, Text, Boolean
from database import Base
import enum

class FoodExchangeCategory(str, enum.Enum):
    CEREALS = "cereales"
    LEGUMES = "leguminosas"
    VEGETABLES = "verduras"
    FRUITS = "frutas"
    MEAT = "carnes"
    DAIRY = "lacteos"
    FATS = "grasas"
    SUGARS = "azucares"

class FoodExchange(Base):
    __tablename__ = "food_exchanges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(FoodExchangeCategory), nullable=False)
    
    # Portion information
    portion_size = Column(String)
    portion_weight = Column(Float)  # grams
    
    # Macronutrients per portion
    calories = Column(Float)
    proteins = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)
    fiber = Column(Float)
    
    # Micronutrients per portion (mg unless specified)
    calcium = Column(Float)  # mg
    iron = Column(Float)  # mg
    sodium = Column(Float)  # mg
    potassium = Column(Float)  # mg
    vitamin_a = Column(Float)  # mcg
    vitamin_c = Column(Float)  # mg
    
    # Additional info
    notes = Column(Text)
    is_custom = Column(Boolean, default=False)


