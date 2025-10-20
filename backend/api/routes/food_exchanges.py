from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.food_exchange import FoodExchange, FoodExchangeCategory
from pydantic import BaseModel

router = APIRouter()

# Schemas
class FoodExchangeCreate(BaseModel):
    name: str
    category: FoodExchangeCategory
    portion_size: str
    portion_weight: float
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    fiber: float | None = None
    calcium: float | None = None
    iron: float | None = None
    sodium: float | None = None
    potassium: float | None = None
    vitamin_a: float | None = None
    vitamin_c: float | None = None
    notes: str | None = None
    is_custom: bool = False

class FoodExchangeResponse(BaseModel):
    id: int
    name: str
    category: FoodExchangeCategory
    portion_size: str
    portion_weight: float
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    fiber: float | None
    calcium: float | None
    iron: float | None
    sodium: float | None
    potassium: float | None
    vitamin_a: float | None
    vitamin_c: float | None
    notes: str | None
    is_custom: bool

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=FoodExchangeResponse)
def create_food_exchange(food_exchange: FoodExchangeCreate, db: Session = Depends(get_db)):
    """Crear un nuevo intercambio alimenticio"""
    db_food_exchange = FoodExchange(**food_exchange.model_dump())
    db.add(db_food_exchange)
    db.commit()
    db.refresh(db_food_exchange)
    return db_food_exchange

@router.get("/", response_model=List[FoodExchangeResponse])
def get_food_exchanges(category: FoodExchangeCategory | None = None, db: Session = Depends(get_db)):
    """Obtener lista de intercambios alimenticios"""
    query = db.query(FoodExchange)
    if category:
        query = query.filter(FoodExchange.category == category)
    food_exchanges = query.all()
    return food_exchanges

@router.get("/{exchange_id}", response_model=FoodExchangeResponse)
def get_food_exchange(exchange_id: int, db: Session = Depends(get_db)):
    """Obtener un intercambio alimenticio específico"""
    food_exchange = db.query(FoodExchange).filter(FoodExchange.id == exchange_id).first()
    if not food_exchange:
        raise HTTPException(status_code=404, detail="Intercambio no encontrado")
    return food_exchange

@router.put("/{exchange_id}", response_model=FoodExchangeResponse)
def update_food_exchange(exchange_id: int, exchange_data: FoodExchangeCreate, db: Session = Depends(get_db)):
    """Actualizar un intercambio alimenticio"""
    food_exchange = db.query(FoodExchange).filter(FoodExchange.id == exchange_id).first()
    if not food_exchange:
        raise HTTPException(status_code=404, detail="Intercambio no encontrado")
    
    for key, value in exchange_data.model_dump().items():
        setattr(food_exchange, key, value)
    
    db.commit()
    db.refresh(food_exchange)
    return food_exchange

@router.delete("/{exchange_id}")
def delete_food_exchange(exchange_id: int, db: Session = Depends(get_db)):
    """Eliminar un intercambio alimenticio"""
    food_exchange = db.query(FoodExchange).filter(FoodExchange.id == exchange_id).first()
    if not food_exchange:
        raise HTTPException(status_code=404, detail="Intercambio no encontrado")
    
    db.delete(food_exchange)
    db.commit()
    return {"message": "Intercambio eliminado exitosamente"}

@router.post("/seed-default-exchanges")
def seed_default_exchanges(db: Session = Depends(get_db)):
    """Crear intercambios alimenticios predefinidos"""
    default_exchanges = [
        # CEREALES
        {"name": "Arroz blanco cocido", "category": FoodExchangeCategory.CEREALS, "portion_size": "1/2 taza", "portion_weight": 100, "calories": 130, "proteins": 2.7, "carbohydrates": 28, "fats": 0.3, "fiber": 0.4},
        {"name": "Pan integral", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 rebanada", "portion_weight": 30, "calories": 80, "proteins": 4, "carbohydrates": 15, "fats": 1, "fiber": 2},
        {"name": "Avena en hojuelas", "category": FoodExchangeCategory.CEREALS, "portion_size": "1/2 taza", "portion_weight": 40, "calories": 150, "proteins": 5, "carbohydrates": 27, "fats": 3, "fiber": 4},
        {"name": "Pasta cocida", "category": FoodExchangeCategory.CEREALS, "portion_size": "1/2 taza", "portion_weight": 70, "calories": 110, "proteins": 4, "carbohydrates": 22, "fats": 0.6, "fiber": 1.3},
        {"name": "Arepa pequeña", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 unidad", "portion_weight": 50, "calories": 140, "proteins": 3, "carbohydrates": 30, "fats": 1, "fiber": 2},
        
        # LEGUMINOSAS
        {"name": "Frijoles cocidos", "category": FoodExchangeCategory.LEGUMES, "portion_size": "1/2 taza", "portion_weight": 90, "calories": 115, "proteins": 8, "carbohydrates": 20, "fats": 0.5, "fiber": 7},
        {"name": "Lentejas cocidas", "category": FoodExchangeCategory.LEGUMES, "portion_size": "1/2 taza", "portion_weight": 100, "calories": 115, "proteins": 9, "carbohydrates": 20, "fats": 0.4, "fiber": 8},
        {"name": "Garbanzos cocidos", "category": FoodExchangeCategory.LEGUMES, "portion_size": "1/2 taza", "portion_weight": 80, "calories": 135, "proteins": 7, "carbohydrates": 23, "fats": 2, "fiber": 6},
        
        # VERDURAS
        {"name": "Brócoli cocido", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1 taza", "portion_weight": 150, "calories": 55, "proteins": 4, "carbohydrates": 11, "fats": 0.6, "fiber": 5},
        {"name": "Zanahoria cocida", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1/2 taza", "portion_weight": 80, "calories": 27, "proteins": 0.6, "carbohydrates": 6, "fats": 0.1, "fiber": 2.3},
        {"name": "Espinaca cocida", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1 taza", "portion_weight": 180, "calories": 41, "proteins": 5, "carbohydrates": 7, "fats": 0.5, "fiber": 4},
        {"name": "Tomate", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1 unidad mediana", "portion_weight": 120, "calories": 22, "proteins": 1, "carbohydrates": 5, "fats": 0.2, "fiber": 1.5},
        {"name": "Lechuga", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "2 tazas", "portion_weight": 100, "calories": 15, "proteins": 1.4, "carbohydrates": 2.9, "fats": 0.2, "fiber": 1.3},
        
        # FRUTAS
        {"name": "Manzana", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad mediana", "portion_weight": 180, "calories": 95, "proteins": 0.5, "carbohydrates": 25, "fats": 0.3, "fiber": 4.4},
        {"name": "Banana", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad mediana", "portion_weight": 120, "calories": 105, "proteins": 1.3, "carbohydrates": 27, "fats": 0.4, "fiber": 3},
        {"name": "Naranja", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad mediana", "portion_weight": 130, "calories": 62, "proteins": 1.2, "carbohydrates": 15, "fats": 0.2, "fiber": 3},
        {"name": "Papaya", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 taza", "portion_weight": 140, "calories": 55, "proteins": 0.9, "carbohydrates": 14, "fats": 0.2, "fiber": 2.5},
        {"name": "Mango", "category": FoodExchangeCategory.FRUITS, "portion_size": "1/2 taza", "portion_weight": 85, "calories": 50, "proteins": 0.4, "carbohydrates": 13, "fats": 0.2, "fiber": 1.4},
        
        # CARNES
        {"name": "Pechuga de pollo sin piel", "category": FoodExchangeCategory.MEAT, "portion_size": "90g", "portion_weight": 90, "calories": 165, "proteins": 31, "carbohydrates": 0, "fats": 3.6, "fiber": 0},
        {"name": "Carne de res magra", "category": FoodExchangeCategory.MEAT, "portion_size": "90g", "portion_weight": 90, "calories": 184, "proteins": 26, "carbohydrates": 0, "fats": 8, "fiber": 0},
        {"name": "Pescado blanco", "category": FoodExchangeCategory.MEAT, "portion_size": "90g", "portion_weight": 90, "calories": 90, "proteins": 19, "carbohydrates": 0, "fats": 1.2, "fiber": 0},
        {"name": "Salmón", "category": FoodExchangeCategory.MEAT, "portion_size": "90g", "portion_weight": 90, "calories": 175, "proteins": 25, "carbohydrates": 0, "fats": 8, "fiber": 0},
        {"name": "Atún en agua", "category": FoodExchangeCategory.MEAT, "portion_size": "90g", "portion_weight": 90, "calories": 100, "proteins": 22, "carbohydrates": 0, "fats": 1, "fiber": 0},
        {"name": "Huevo entero", "category": FoodExchangeCategory.MEAT, "portion_size": "1 unidad", "portion_weight": 50, "calories": 72, "proteins": 6, "carbohydrates": 0.4, "fats": 5, "fiber": 0},
        
        # LÁCTEOS
        {"name": "Leche descremada", "category": FoodExchangeCategory.DAIRY, "portion_size": "1 taza", "portion_weight": 240, "calories": 83, "proteins": 8, "carbohydrates": 12, "fats": 0.2, "fiber": 0},
        {"name": "Yogur natural bajo en grasa", "category": FoodExchangeCategory.DAIRY, "portion_size": "1 taza", "portion_weight": 245, "calories": 154, "proteins": 13, "carbohydrates": 17, "fats": 3.8, "fiber": 0},
        {"name": "Queso fresco", "category": FoodExchangeCategory.DAIRY, "portion_size": "30g", "portion_weight": 30, "calories": 74, "proteins": 5, "carbohydrates": 1, "fats": 6, "fiber": 0},
        
        # GRASAS
        {"name": "Aceite de oliva", "category": FoodExchangeCategory.FATS, "portion_size": "1 cucharadita", "portion_weight": 5, "calories": 45, "proteins": 0, "carbohydrates": 0, "fats": 5, "fiber": 0},
        {"name": "Aguacate", "category": FoodExchangeCategory.FATS, "portion_size": "1/4 unidad", "portion_weight": 50, "calories": 80, "proteins": 1, "carbohydrates": 4, "fats": 7, "fiber": 3.4},
        {"name": "Almendras", "category": FoodExchangeCategory.FATS, "portion_size": "10 unidades", "portion_weight": 14, "calories": 82, "proteins": 3, "carbohydrates": 3, "fats": 7, "fiber": 1.7},
        {"name": "Nueces", "category": FoodExchangeCategory.FATS, "portion_size": "7 mitades", "portion_weight": 14, "calories": 92, "proteins": 2, "carbohydrates": 2, "fats": 9, "fiber": 1},
    ]
    
    created_exchanges = []
    for exchange_data in default_exchanges:
        existing = db.query(FoodExchange).filter(
            FoodExchange.name == exchange_data["name"],
            FoodExchange.category == exchange_data["category"]
        ).first()
        if not existing:
            db_exchange = FoodExchange(**exchange_data)
            db.add(db_exchange)
            created_exchanges.append(exchange_data["name"])
    
    db.commit()
    return {"message": f"Intercambios creados: {len(created_exchanges)}", "exchanges": created_exchanges}

@router.post("/seed-colombian-foods")
def seed_colombian_foods(db: Session = Depends(get_db)):
    """Agregar alimentos típicos colombianos con micronutrientes completos"""
    colombian_foods = [
        # CEREALES Y TUBÉRCULOS COLOMBIANOS
        {"name": "Arepa de maíz blanco", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 unidad mediana", "portion_weight": 70, "calories": 162, "proteins": 3.5, "carbohydrates": 33, "fats": 1.5, "fiber": 2.8, "calcium": 15, "iron": 1.2, "sodium": 280, "potassium": 95, "vitamin_a": 0, "vitamin_c": 0, "notes": "Típica del desayuno colombiano"},
        {"name": "Arepa de maíz amarillo", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 unidad mediana", "portion_weight": 70, "calories": 155, "proteins": 3.2, "carbohydrates": 31, "fats": 1.8, "fiber": 3.2, "calcium": 18, "iron": 1.4, "sodium": 260, "potassium": 105, "vitamin_a": 28, "vitamin_c": 0, "notes": "Rico en betacarotenos"},
        {"name": "Pandebono", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 unidad", "portion_weight": 50, "calories": 148, "proteins": 4.5, "carbohydrates": 20, "fats": 5.5, "fiber": 1, "calcium": 85, "iron": 0.8, "sodium": 180, "potassium": 65, "vitamin_a": 15, "vitamin_c": 0, "notes": "Pan de yuca con queso"},
        {"name": "Almojábana", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 unidad", "portion_weight": 55, "calories": 152, "proteins": 5, "carbohydrates": 18, "fats": 6, "fiber": 0.8, "calcium": 95, "iron": 0.9, "sodium": 195, "potassium": 70, "vitamin_a": 20, "vitamin_c": 0, "notes": "Pan de queso colombiano"},
        {"name": "Buñuelo", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 unidad", "portion_weight": 30, "calories": 95, "proteins": 2.8, "carbohydrates": 12, "fats": 3.5, "fiber": 0.5, "calcium": 42, "iron": 0.6, "sodium": 125, "potassium": 38, "vitamin_a": 12, "vitamin_c": 0, "notes": "Típico de Navidad"},
        {"name": "Yuca cocida", "category": FoodExchangeCategory.CEREALS, "portion_size": "1/2 taza", "portion_weight": 100, "calories": 159, "proteins": 1.4, "carbohydrates": 38, "fats": 0.3, "fiber": 1.8, "calcium": 16, "iron": 0.3, "sodium": 14, "potassium": 271, "vitamin_a": 1, "vitamin_c": 20.7, "notes": "Fuente de carbohidratos"},
        {"name": "Plátano verde cocido", "category": FoodExchangeCategory.CEREALS, "portion_size": "1/2 taza", "portion_weight": 90, "calories": 116, "proteins": 1.2, "carbohydrates": 31, "fats": 0.2, "fiber": 2.3, "calcium": 3, "iron": 0.6, "sodium": 4, "potassium": 465, "vitamin_a": 56, "vitamin_c": 18.4, "notes": "Alto en potasio"},
        {"name": "Plátano maduro cocido", "category": FoodExchangeCategory.CEREALS, "portion_size": "1/2 taza", "portion_weight": 90, "calories": 122, "proteins": 1, "carbohydrates": 32, "fats": 0.3, "fiber": 2.6, "calcium": 3, "iron": 0.5, "sodium": 3, "potassium": 358, "vitamin_a": 112, "vitamin_c": 15.6, "notes": "Más dulce que el verde"},
        {"name": "Patacón", "category": FoodExchangeCategory.CEREALS, "portion_size": "1 unidad", "portion_weight": 45, "calories": 135, "proteins": 0.8, "carbohydrates": 20, "fats": 5.5, "fiber": 1.5, "calcium": 2, "iron": 0.4, "sodium": 85, "potassium": 280, "vitamin_a": 35, "vitamin_c": 11, "notes": "Plátano verde frito y aplastado"},
        {"name": "Papa criolla", "category": FoodExchangeCategory.CEREALS, "portion_size": "4 unidades", "portion_weight": 100, "calories": 77, "proteins": 2, "carbohydrates": 17, "fats": 0.1, "fiber": 2.2, "calcium": 12, "iron": 0.8, "sodium": 6, "potassium": 421, "vitamin_a": 2, "vitamin_c": 19.7, "notes": "Papa típica colombiana, amarilla"},
        
        # LEGUMINOSAS COLOMBIANAS
        {"name": "Fríjol cargamanto", "category": FoodExchangeCategory.LEGUMES, "portion_size": "1/2 taza cocido", "portion_weight": 90, "calories": 125, "proteins": 8.5, "carbohydrates": 22, "fats": 0.6, "fiber": 7.5, "calcium": 48, "iron": 2.8, "sodium": 2, "potassium": 395, "vitamin_a": 0, "vitamin_c": 1.2, "notes": "Variedad colombiana de frijol"},
        {"name": "Fríjol rojo", "category": FoodExchangeCategory.LEGUMES, "portion_size": "1/2 taza cocido", "portion_weight": 90, "calories": 115, "proteins": 8, "carbohydrates": 20, "fats": 0.5, "fiber": 7, "calcium": 45, "iron": 2.6, "sodium": 2, "potassium": 358, "vitamin_a": 0, "vitamin_c": 1, "notes": "Común en todo Colombia"},
        {"name": "Arveja verde", "category": FoodExchangeCategory.LEGUMES, "portion_size": "1/2 taza cocida", "portion_weight": 80, "calories": 67, "proteins": 4.3, "carbohydrates": 12.5, "fats": 0.2, "fiber": 4.4, "calcium": 25, "iron": 1.5, "sodium": 4, "potassium": 244, "vitamin_a": 38, "vitamin_c": 13.8, "notes": "Típica en sopas colombianas"},
        
        # VERDURAS COLOMBIANAS
        {"name": "Ahuyama (Calabaza)", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1 taza cocida", "portion_weight": 150, "calories": 49, "proteins": 1.8, "carbohydrates": 12, "fats": 0.2, "fiber": 2.7, "calcium": 21, "iron": 1.4, "sodium": 1, "potassium": 564, "vitamin_a": 1144, "vitamin_c": 11.5, "notes": "Rica en vitamina A"},
        {"name": "Chontaduro", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1 unidad", "portion_weight": 50, "calories": 93, "proteins": 1.5, "carbohydrates": 15, "fats": 3.5, "fiber": 2.8, "calcium": 28, "iron": 0.7, "sodium": 8, "potassium": 485, "vitamin_a": 285, "vitamin_c": 45, "notes": "Fruta del pacífico colombiano"},
        {"name": "Habichuela", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1 taza cocida", "portion_weight": 125, "calories": 44, "proteins": 2.4, "carbohydrates": 10, "fats": 0.1, "fiber": 3.4, "calcium": 58, "iron": 1.6, "sodium": 1, "potassium": 209, "vitamin_a": 35, "vitamin_c": 16.3, "notes": "Vainita o judía verde"},
        {"name": "Cidra papa", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1 taza cocida", "portion_weight": 150, "calories": 28, "proteins": 1.1, "carbohydrates": 6.5, "fats": 0.2, "fiber": 1.8, "calcium": 17, "iron": 0.4, "sodium": 2, "potassium": 218, "vitamin_a": 5, "vitamin_c": 17.5, "notes": "Usada en sancochos"},
        {"name": "Cilantro", "category": FoodExchangeCategory.VEGETABLES, "portion_size": "1/4 taza picado", "portion_weight": 10, "calories": 2, "proteins": 0.2, "carbohydrates": 0.4, "fats": 0, "fiber": 0.3, "calcium": 7, "iron": 0.2, "sodium": 5, "potassium": 52, "vitamin_a": 68, "vitamin_c": 2.7, "notes": "Hierba aromática esencial"},
        
        # FRUTAS TROPICALES COLOMBIANAS
        {"name": "Guanábana", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 taza pulpa", "portion_weight": 140, "calories": 93, "proteins": 1.4, "carbohydrates": 23.6, "fats": 0.4, "fiber": 4.5, "calcium": 19, "iron": 0.8, "sodium": 17, "potassium": 395, "vitamin_a": 1, "vitamin_c": 29.4, "notes": "Fruta tropical ácida"},
        {"name": "Lulo", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad", "portion_weight": 100, "calories": 25, "proteins": 0.5, "carbohydrates": 6, "fats": 0.1, "fiber": 1.8, "calcium": 8, "iron": 0.4, "sodium": 2, "potassium": 185, "vitamin_a": 65, "vitamin_c": 25, "notes": "Naranjilla, típico de jugos"},
        {"name": "Gulupa", "category": FoodExchangeCategory.FRUITS, "portion_size": "2 unidades", "portion_weight": 90, "calories": 44, "proteins": 1, "carbohydrates": 10.5, "fats": 0.3, "fiber": 4.8, "calcium": 5, "iron": 0.7, "sodium": 16, "potassium": 245, "vitamin_a": 72, "vitamin_c": 18, "notes": "Maracuyá morado"},
        {"name": "Granadilla", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad", "portion_weight": 110, "calories": 54, "proteins": 1.2, "carbohydrates": 12.8, "fats": 0.2, "fiber": 3.2, "calcium": 8, "iron": 0.9, "sodium": 18, "potassium": 270, "vitamin_a": 85, "vitamin_c": 22, "notes": "Fruta de la pasión dulce"},
        {"name": "Curuba", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad", "portion_weight": 100, "calories": 38, "proteins": 0.9, "carbohydrates": 9, "fats": 0.2, "fiber": 2.5, "calcium": 6, "iron": 0.5, "sodium": 12, "potassium": 215, "vitamin_a": 55, "vitamin_c": 35, "notes": "Banana passionfruit"},
        {"name": "Uchuva", "category": FoodExchangeCategory.FRUITS, "portion_size": "1/2 taza", "portion_weight": 70, "calories": 37, "proteins": 1.1, "carbohydrates": 8, "fats": 0.5, "fiber": 2.8, "calcium": 5, "iron": 0.7, "sodium": 1, "potassium": 162, "vitamin_a": 105, "vitamin_c": 15.4, "notes": "Golden berry, alta en antioxidantes"},
        {"name": "Feijoa", "category": FoodExchangeCategory.FRUITS, "portion_size": "2 unidades", "portion_weight": 100, "calories": 55, "proteins": 1.2, "carbohydrates": 13, "fats": 0.4, "fiber": 6.4, "calcium": 17, "iron": 0.3, "sodium": 3, "potassium": 172, "vitamin_a": 4, "vitamin_c": 32.9, "notes": "Pineapple guava"},
        {"name": "Zapote", "category": FoodExchangeCategory.FRUITS, "portion_size": "1/2 taza pulpa", "portion_weight": 90, "calories": 75, "proteins": 0.9, "carbohydrates": 19, "fats": 0.2, "fiber": 3.5, "calcium": 18, "iron": 0.4, "sodium": 8, "potassium": 225, "vitamin_a": 128, "vitamin_c": 28.5, "notes": "Mamey sapote"},
        {"name": "Pitaya amarilla", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad", "portion_weight": 120, "calories": 58, "proteins": 1.4, "carbohydrates": 13, "fats": 0.5, "fiber": 3.6, "calcium": 10, "iron": 0.4, "sodium": 2, "potassium": 185, "vitamin_a": 2, "vitamin_c": 28, "notes": "Dragon fruit colombiana"},
        {"name": "Maracuyá", "category": FoodExchangeCategory.FRUITS, "portion_size": "2 unidades", "portion_weight": 90, "calories": 42, "proteins": 1, "carbohydrates": 10, "fats": 0.3, "fiber": 4.5, "calcium": 5, "iron": 0.7, "sodium": 16, "potassium": 245, "vitamin_a": 70, "vitamin_c": 17.5, "notes": "Passion fruit amarillo"},
        {"name": "Guayaba", "category": FoodExchangeCategory.FRUITS, "portion_size": "1 unidad", "portion_weight": 100, "calories": 68, "proteins": 2.6, "carbohydrates": 14.3, "fats": 1, "fiber": 5.4, "calcium": 18, "iron": 0.3, "sodium": 2, "potassium": 417, "vitamin_a": 31, "vitamin_c": 228.3, "notes": "Altísima en vitamina C"},
        
        # CARNES Y PROTEÍNAS COLOMBIANAS
        {"name": "Chicharrón", "category": FoodExchangeCategory.MEAT, "portion_size": "30g", "portion_weight": 30, "calories": 185, "proteins": 8.5, "carbohydrates": 0, "fats": 17, "fiber": 0, "calcium": 5, "iron": 0.4, "sodium": 280, "potassium": 85, "vitamin_a": 0, "vitamin_c": 0, "notes": "Alto en grasa, consumo ocasional"},
        {"name": "Bocadillo (guayaba)", "category": FoodExchangeCategory.SUGARS, "portion_size": "1 tajada", "portion_weight": 25, "calories": 82, "proteins": 0.3, "carbohydrates": 20, "fats": 0.1, "fiber": 1.8, "calcium": 8, "iron": 0.2, "sodium": 8, "potassium": 105, "vitamin_a": 12, "vitamin_c": 35, "notes": "Dulce típico de guayaba"},
        
        # LÁCTEOS COLOMBIANOS
        {"name": "Queso campesino", "category": FoodExchangeCategory.DAIRY, "portion_size": "30g", "portion_weight": 30, "calories": 85, "proteins": 6, "carbohydrates": 0.8, "fats": 6.5, "fiber": 0, "calcium": 195, "iron": 0.1, "sodium": 185, "potassium": 28, "vitamin_a": 48, "vitamin_c": 0, "notes": "Queso fresco colombiano"},
        {"name": "Queso costeño", "category": FoodExchangeCategory.DAIRY, "portion_size": "30g", "portion_weight": 30, "calories": 92, "proteins": 5.5, "carbohydrates": 1, "fats": 7.5, "fiber": 0, "calcium": 175, "iron": 0.1, "sodium": 425, "potassium": 25, "vitamin_a": 42, "vitamin_c": 0, "notes": "Queso salado de la costa"},
        {"name": "Cuajada", "category": FoodExchangeCategory.DAIRY, "portion_size": "30g", "portion_weight": 30, "calories": 78, "proteins": 5.8, "carbohydrates": 0.9, "fats": 6, "fiber": 0, "calcium": 188, "iron": 0.1, "sodium": 95, "potassium": 30, "vitamin_a": 45, "vitamin_c": 0, "notes": "Requesón colombiano"},
        
        # GRASAS COLOMBIANAS
        {"name": "Aguacate Hass", "category": FoodExchangeCategory.FATS, "portion_size": "1/4 unidad", "portion_weight": 50, "calories": 80, "proteins": 1, "carbohydrates": 4, "fats": 7.5, "fiber": 3.4, "calcium": 6, "iron": 0.3, "sodium": 4, "potassium": 245, "vitamin_a": 7, "vitamin_c": 5, "notes": "Variedad más cremosa"},
        {"name": "Maní colombiano", "category": FoodExchangeCategory.FATS, "portion_size": "15 unidades", "portion_weight": 14, "calories": 82, "proteins": 3.7, "carbohydrates": 3, "fats": 7, "fiber": 1.2, "calcium": 8, "iron": 0.5, "sodium": 1, "potassium": 95, "vitamin_a": 0, "vitamin_c": 0, "notes": "Cacahuate local"},
    ]
    
    created_foods = []
    for food_data in colombian_foods:
        existing = db.query(FoodExchange).filter(
            FoodExchange.name == food_data["name"]
        ).first()
        if not existing:
            db_food = FoodExchange(**food_data)
            db.add(db_food)
            created_foods.append(food_data["name"])
    
    db.commit()
    return {
        "message": f"Alimentos colombianos agregados: {len(created_foods)}", 
        "foods": created_foods,
        "total": len(colombian_foods)
    }


