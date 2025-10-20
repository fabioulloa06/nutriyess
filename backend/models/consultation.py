from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    consultation_date = Column(DateTime, default=datetime.now)
    
    # Basic measurements
    weight = Column(Float)
    height = Column(Float)
    bmi = Column(Float)
    weight_change = Column(Float)  # Cambio desde última consulta
    
    # Circumferences (cm)
    waist_circumference = Column(Float)
    hip_circumference = Column(Float)
    arm_circumference = Column(Float)
    thigh_circumference = Column(Float)
    calf_circumference = Column(Float)
    
    # Skinfolds (mm)
    triceps_skinfold = Column(Float)
    biceps_skinfold = Column(Float)
    subscapular_skinfold = Column(Float)
    suprailiac_skinfold = Column(Float)
    abdominal_skinfold = Column(Float)
    
    # Body composition
    body_fat_percentage = Column(Float)
    muscle_mass = Column(Float)
    
    # Activity level changes
    activity_level_changed = Column(Integer, default=0)  # 0=no, 1=yes
    new_activity_level = Column(String)
    
    # Calculated values
    caloric_requirement = Column(Float)
    healthy_weight = Column(Float)
    adjusted_weight = Column(Float)
    
    # Clinical notes
    notes = Column(Text)
    recommendations = Column(Text)
    diet_plan = Column(Text)
    clinical_observations = Column(Text)
    
    # Follow-up
    next_appointment = Column(DateTime)
    follow_up_notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="consultations")


