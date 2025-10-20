from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta
import enum

class UserRole(str, enum.Enum):
    nutricionista = "nutricionista"
    admin = "admin"

class SubscriptionStatus(str, enum.Enum):
    trial = "trial"
    active = "active"
    expired = "expired"
    cancelled = "cancelled"

class SubscriptionPlan(str, enum.Enum):
    basic = "basic"
    professional = "professional"
    enterprise = "enterprise"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    role = Column(Enum(UserRole), default=UserRole.nutricionista)
    
    # Subscription information
    subscription_status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.trial)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.basic)
    trial_start_date = Column(DateTime, default=datetime.now)
    trial_end_date = Column(DateTime, default=lambda: datetime.now() + timedelta(days=30))
    subscription_start_date = Column(DateTime)
    subscription_end_date = Column(DateTime)
    
    # Profile information
    professional_license = Column(String)  # Licencia profesional
    specialization = Column(String)  # Especialización
    clinic_name = Column(String)  # Nombre de la clínica
    clinic_address = Column(Text)  # Dirección de la clínica
    bio = Column(Text)  # Biografía profesional
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)
    
    # Relationships
    patients = relationship("Patient", back_populates="nutritionist", cascade="all, delete-orphan")
    consultations = relationship("Consultation", back_populates="nutritionist", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="nutritionist", cascade="all, delete-orphan")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    nutritionist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Personal information
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    identification = Column(String, index=True)
    birth_date = Column(DateTime)
    gender = Column(Enum('masculino', 'femenino', 'otro'), default='masculino')
    
    # Contact information
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    
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
    
    # Medical information
    medical_history = Column(Text)
    nutritional_history = Column(Text)
    allergies = Column(Text)
    medications = Column(Text)
    patient_type = Column(Enum('sano', 'hospitalizado', 'uci', 'deportista', 'adolescente', 'adulto_mayor', 'embarazada'), default='sano')
    activity_level = Column(Enum('sedentario', 'ligero', 'moderado', 'activo', 'muy_activo'), default='moderado')
    is_vegetarian = Column(Integer, default=0)  # 0: Omnivore, 1: Vegetarian, 2: Vegan
    has_diabetes = Column(Integer, default=0)
    has_hypertension = Column(Integer, default=0)
    has_bloating = Column(Integer, default=0)
    other_conditions = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    nutritionist = relationship("User", back_populates="patients")
    consultations = relationship("Consultation", back_populates="patient", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="patient", cascade="all, delete-orphan")
    preferences = relationship("PatientPreferences", back_populates="patient", uselist=False, cascade="all, delete-orphan")
