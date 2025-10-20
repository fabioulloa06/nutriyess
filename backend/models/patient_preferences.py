from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base

class PatientPreferences(Base):
    __tablename__ = "patient_preferences"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True)
    
    # Alimentos favoritos y no favoritos
    favorite_foods = Column(Text)  # JSON string con lista de alimentos
    disliked_foods = Column(Text)  # JSON string con lista de alimentos
    allergies = Column(Text)  # JSON string con alergias
    
    # Preferencias de cocina
    preferred_cooking_methods = Column(Text)  # hervido, asado, al vapor, frito, etc.
    
    # Restricciones
    cultural_restrictions = Column(Text)  # Restricciones culturales/religiosas
    budget_level = Column(String)  # bajo, medio, alto
    cooking_time_available = Column(String)  # poco (<15min), medio (15-30min), mucho (>30min)
    
    # Preferencias de sabor (escala 1-5)
    likes_sweet = Column(Integer, default=3)  # 1=no le gusta, 5=le encanta
    likes_salty = Column(Integer, default=3)
    likes_spicy = Column(Integer, default=3)
    likes_sour = Column(Integer, default=3)
    likes_bitter = Column(Integer, default=3)
    
    # Texturas preferidas
    prefers_soft_textures = Column(Boolean, default=True)
    prefers_crunchy_textures = Column(Boolean, default=True)
    
    # Horarios de comida
    breakfast_time = Column(String)  # HH:MM
    lunch_time = Column(String)
    dinner_time = Column(String)
    snacks_per_day = Column(Integer, default=2)
    
    # Notas adicionales
    additional_notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="preferences")
