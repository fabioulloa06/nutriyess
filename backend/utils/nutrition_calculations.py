from datetime import date
from enum import Enum

class Gender(str, Enum):
    MALE = "masculino"
    FEMALE = "femenino"

class PatientType(str, Enum):
    HEALTHY = "sano"
    HOSPITALIZED = "hospitalizado"
    ICU = "uci"
    ATHLETE = "deportista"
    ADOLESCENT = "adolescente"
    ELDERLY = "adulto_mayor"
    PREGNANT = "embarazada"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentario"
    LIGHT = "ligero"
    MODERATE = "moderado"
    ACTIVE = "activo"
    VERY_ACTIVE = "muy_activo"


def calculate_age(birth_date: date) -> int:
    """Calcula la edad a partir de la fecha de nacimiento"""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def calculate_bmi(weight: float, height: float) -> float:
    """
    Calcula el IMC (Índice de Masa Corporal)
    weight: peso en kg
    height: altura en cm
    """
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)


def get_bmi_category(bmi: float, age: int) -> str:
    """
    Categoriza el IMC según rangos de edad
    """
    if age < 18:
        # Para niños y adolescentes se usan percentiles, esto es una simplificación
        if bmi < 18.5:
            return "Bajo peso"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
    elif age < 65:
        # Adultos
        if bmi < 18.5:
            return "Bajo peso"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Sobrepeso"
        elif bmi < 35:
            return "Obesidad I"
        elif bmi < 40:
            return "Obesidad II"
        else:
            return "Obesidad III"
    else:
        # Adultos mayores (rangos más permisivos)
        if bmi < 23:
            return "Bajo peso"
        elif bmi < 28:
            return "Normal"
        elif bmi < 33:
            return "Sobrepeso"
        else:
            return "Obesidad"


def calculate_ideal_weight(height: float, gender: str) -> float:
    """
    Calcula el peso ideal usando la fórmula de Devine
    height: altura en cm
    gender: masculino o femenino
    """
    height_inches = height / 2.54
    
    if gender.lower() in ["masculino", "male"]:
        # Hombres: 50 kg + 2.3 kg por cada pulgada sobre 5 pies (60 pulgadas)
        ideal_weight = 50 + 2.3 * (height_inches - 60)
    else:
        # Mujeres: 45.5 kg + 2.3 kg por cada pulgada sobre 5 pies (60 pulgadas)
        ideal_weight = 45.5 + 2.3 * (height_inches - 60)
    
    return round(max(ideal_weight, 45), 2)


def calculate_adjusted_weight(current_weight: float, ideal_weight: float) -> float:
    """
    Calcula el peso ajustado (usado cuando hay obesidad)
    Fórmula: Peso ideal + 0.25 * (Peso actual - Peso ideal)
    """
    if current_weight <= ideal_weight:
        return current_weight
    
    adjusted = ideal_weight + 0.25 * (current_weight - ideal_weight)
    return round(adjusted, 2)


def calculate_tmb(weight: float, height: float, age: int, gender: str) -> float:
    """
    Calcula la Tasa Metabólica Basal usando la ecuación de Harris-Benedict revisada
    """
    if gender.lower() in ["masculino", "male"]:
        tmb = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        tmb = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return round(tmb, 2)


def get_activity_factor(activity_level: str) -> float:
    """
    Obtiene el factor de actividad física
    """
    factors = {
        "sedentario": 1.2,
        "ligero": 1.375,
        "moderado": 1.55,
        "activo": 1.725,
        "muy_activo": 1.9
    }
    return factors.get(activity_level.lower(), 1.55)


def get_stress_factor(patient_type: str) -> float:
    """
    Obtiene el factor de estrés según el tipo de paciente
    """
    factors = {
        "sano": 1.0,
        "hospitalizado": 1.2,
        "uci": 1.5,
        "deportista": 1.3,
        "adolescente": 1.15,
        "adulto_mayor": 1.0,
        "embarazada": 1.15
    }
    return factors.get(patient_type.lower(), 1.0)


def calculate_caloric_requirement(
    weight: float,
    height: float,
    age: int,
    gender: str,
    activity_level: str = "moderado",
    patient_type: str = "sano",
    use_adjusted_weight: bool = False
) -> dict:
    """
    Calcula el requerimiento calórico diario
    Retorna un diccionario con todos los valores calculados
    """
    # Calcular TMB
    tmb = calculate_tmb(weight, height, age, gender)
    
    # Obtener factores
    activity_factor = get_activity_factor(activity_level)
    stress_factor = get_stress_factor(patient_type)
    
    # Calcular requerimiento energético total
    caloric_requirement = tmb * activity_factor * stress_factor
    
    # Ajustes especiales
    if patient_type == "embarazada":
        # Añadir calorías adicionales según trimestre (promedio)
        caloric_requirement += 300
    elif patient_type == "deportista":
        # Los deportistas pueden necesitar más según intensidad
        caloric_requirement *= 1.1
    
    # Calcular distribución de macronutrientes
    # Proteínas: 15-20% (usar 1.2-2.0 g/kg según tipo de paciente)
    if patient_type == "deportista":
        protein_per_kg = 1.8
    elif patient_type == "adulto_mayor":
        protein_per_kg = 1.2
    else:
        protein_per_kg = 1.0
    
    proteins_g = weight * protein_per_kg
    proteins_kcal = proteins_g * 4
    
    # Grasas: 25-30%
    fats_kcal = caloric_requirement * 0.275
    fats_g = fats_kcal / 9
    
    # Carbohidratos: resto
    carbs_kcal = caloric_requirement - proteins_kcal - fats_kcal
    carbs_g = carbs_kcal / 4
    
    return {
        "tmb": round(tmb, 2),
        "caloric_requirement": round(caloric_requirement, 2),
        "proteins_g": round(proteins_g, 2),
        "carbs_g": round(carbs_g, 2),
        "fats_g": round(fats_g, 2),
        "activity_factor": activity_factor,
        "stress_factor": stress_factor
    }


