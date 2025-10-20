from sqlalchemy import Column, Integer, String, Float, Date, Enum, Text
from sqlalchemy.orm import relationship
from database import Base
import enum

class Gender(str, enum.Enum):
    MALE = "masculino"
    FEMALE = "femenino"
    OTHER = "otro"

class ActivityLevel(str, enum.Enum):
    SEDENTARY = "sedentario"
    LIGHT = "ligero"
    MODERATE = "moderado"
    ACTIVE = "activo"
    VERY_ACTIVE = "muy_activo"

class PatientType(str, enum.Enum):
    HEALTHY = "sano"
    HOSPITALIZED = "hospitalizado"
    ICU = "uci"
    ATHLETE = "deportista"
    ADOLESCENT = "adolescente"
    ELDERLY = "adulto_mayor"
    PREGNANT = "embarazada"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    identification = Column(String, unique=True, index=True)
    birth_date = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    
    # Anthropometric data
    weight = Column(Float, nullable=False)  # kg
    height = Column(Float, nullable=False)  # cm
    
    # Additional anthropometric data (optional)
    body_fat_percentage = Column(Float)  # %
    muscle_mass = Column(Float)  # kg
    waist_circumference = Column(Float)  # cm
    hip_circumference = Column(Float)  # cm
    arm_circumference = Column(Float)  # cm
    thigh_circumference = Column(Float)  # cm
    calf_circumference = Column(Float)  # cm
    triceps_skinfold = Column(Float)  # mm
    biceps_skinfold = Column(Float)  # mm
    subscapular_skinfold = Column(Float)  # mm
    suprailiac_skinfold = Column(Float)  # mm
    abdominal_skinfold = Column(Float)  # mm
    
    # Medical history
    medical_history = Column(Text)
    nutritional_history = Column(Text)
    allergies = Column(Text)
    medications = Column(Text)
    
    # Patient type and activity
    patient_type = Column(Enum(PatientType), default=PatientType.HEALTHY)
    activity_level = Column(Enum(ActivityLevel), default=ActivityLevel.MODERATE)
    
    # Dietary preferences
    is_vegetarian = Column(Integer, default=0)  # 0=no, 1=vegetarian, 2=vegan
    
    # Conditions
    has_diabetes = Column(Integer, default=0)
    has_hypertension = Column(Integer, default=0)
    has_bloating = Column(Integer, default=0)
    other_conditions = Column(Text)
    
    # Relationships
    consultations = relationship("Consultation", back_populates="patient", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="patient", cascade="all, delete-orphan")
    preferences = relationship("PatientPreferences", back_populates="patient", uselist=False, cascade="all, delete-orphan")


