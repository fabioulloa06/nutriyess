from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.snack import Snack, SnackCategory
from pydantic import BaseModel

router = APIRouter()

# Schemas
class SnackCreate(BaseModel):
    name: str
    category: SnackCategory | None = None
    description: str | None = None
    recipe: str | None = None
    calories: float | None = None
    proteins: float | None = None
    carbohydrates: float | None = None
    fats: float | None = None
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_diabetic_friendly: bool = False
    is_low_sodium: bool = False
    is_custom: bool = False

class SnackResponse(BaseModel):
    id: int
    name: str
    category: SnackCategory | None
    description: str | None
    recipe: str | None
    calories: float | None
    proteins: float | None
    carbohydrates: float | None
    fats: float | None
    is_vegetarian: bool
    is_vegan: bool
    is_diabetic_friendly: bool
    is_low_sodium: bool
    is_custom: bool

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=SnackResponse)
def create_snack(snack: SnackCreate, db: Session = Depends(get_db)):
    """Crear un nuevo snack"""
    db_snack = Snack(**snack.model_dump())
    db.add(db_snack)
    db.commit()
    db.refresh(db_snack)
    return db_snack

@router.get("/", response_model=List[SnackResponse])
def get_snacks(
    category: SnackCategory | None = None,
    vegetarian: bool | None = None,
    vegan: bool | None = None,
    diabetic_friendly: bool | None = None,
    low_sodium: bool | None = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de snacks con filtros opcionales"""
    query = db.query(Snack)
    
    if category:
        query = query.filter(Snack.category == category)
    if vegetarian is not None:
        query = query.filter(Snack.is_vegetarian == vegetarian)
    if vegan is not None:
        query = query.filter(Snack.is_vegan == vegan)
    if diabetic_friendly is not None:
        query = query.filter(Snack.is_diabetic_friendly == diabetic_friendly)
    if low_sodium is not None:
        query = query.filter(Snack.is_low_sodium == low_sodium)
    
    snacks = query.all()
    return snacks

@router.get("/{snack_id}", response_model=SnackResponse)
def get_snack(snack_id: int, db: Session = Depends(get_db)):
    """Obtener un snack específico"""
    snack = db.query(Snack).filter(Snack.id == snack_id).first()
    if not snack:
        raise HTTPException(status_code=404, detail="Snack no encontrado")
    return snack

@router.put("/{snack_id}", response_model=SnackResponse)
def update_snack(snack_id: int, snack_data: SnackCreate, db: Session = Depends(get_db)):
    """Actualizar un snack"""
    snack = db.query(Snack).filter(Snack.id == snack_id).first()
    if not snack:
        raise HTTPException(status_code=404, detail="Snack no encontrado")
    
    for key, value in snack_data.model_dump().items():
        setattr(snack, key, value)
    
    db.commit()
    db.refresh(snack)
    return snack

@router.delete("/{snack_id}")
def delete_snack(snack_id: int, db: Session = Depends(get_db)):
    """Eliminar un snack"""
    snack = db.query(Snack).filter(Snack.id == snack_id).first()
    if not snack:
        raise HTTPException(status_code=404, detail="Snack no encontrado")
    
    db.delete(snack)
    db.commit()
    return {"message": "Snack eliminado exitosamente"}

@router.post("/seed-default-snacks")
def seed_default_snacks(db: Session = Depends(get_db)):
    """Crear snacks de ejemplo predefinidos"""
    default_snacks = [
        {
            "name": "Yogur con Frutas y Granola",
            "category": SnackCategory.MIXED,
            "description": "Delicioso y nutritivo snack perfecto para cualquier momento del día",
            "recipe": "Ingredientes:\n- 1 taza de yogur griego natural\n- 1/2 taza de frutas frescas (fresas, arándanos, mango)\n- 2 cucharadas de granola casera\n- 1 cucharadita de miel (opcional)\n\nPreparación:\n1. Coloca el yogur en un bowl\n2. Añade las frutas cortadas\n3. Espolvorea la granola encima\n4. Agrega la miel si deseas",
            "calories": 250,
            "proteins": 15,
            "carbohydrates": 35,
            "fats": 6,
            "is_vegetarian": True,
            "is_vegan": False,
            "is_diabetic_friendly": False,
            "is_low_sodium": True
        },
        {
            "name": "Hummus con Vegetales",
            "category": SnackCategory.PROTEIN,
            "description": "Snack alto en proteína vegetal y fibra",
            "recipe": "Ingredientes:\n- 1/2 taza de hummus casero o comercial\n- Zanahorias baby\n- Apio en bastones\n- Pimientos de colores\n- Pepino en rodajas\n\nPreparación:\n1. Lava y corta los vegetales\n2. Sirve el hummus en un bowl pequeño\n3. Acomoda los vegetales alrededor\n4. ¡Listo para disfrutar!",
            "calories": 180,
            "proteins": 8,
            "carbohydrates": 22,
            "fats": 7,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_diabetic_friendly": True,
            "is_low_sodium": True
        },
        {
            "name": "Tostadas de Aguacate",
            "category": SnackCategory.SALTY,
            "description": "Clásico snack saludable y delicioso",
            "recipe": "Ingredientes:\n- 2 rebanadas de pan integral\n- 1/2 aguacate maduro\n- Tomate cherry\n- Limón\n- Sal y pimienta al gusto\n- Semillas de ajonjolí (opcional)\n\nPreparación:\n1. Tuesta el pan\n2. Machaca el aguacate con limón, sal y pimienta\n3. Unta sobre el pan tostado\n4. Decora con tomate cherry y semillas",
            "calories": 220,
            "proteins": 7,
            "carbohydrates": 25,
            "fats": 11,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_diabetic_friendly": True,
            "is_low_sodium": False
        },
        {
            "name": "Energy Balls de Dátiles",
            "category": SnackCategory.SWEET,
            "description": "Bolitas energéticas sin azúcar añadida",
            "recipe": "Ingredientes:\n- 1 taza de dátiles sin semilla\n- 1/2 taza de almendras\n- 2 cucharadas de cacao en polvo\n- 1 cucharada de mantequilla de maní\n- Coco rallado para decorar\n\nPreparación:\n1. Procesa todos los ingredientes en un procesador\n2. Forma bolitas con las manos\n3. Rueda en coco rallado\n4. Refrigera por 30 minutos",
            "calories": 150,
            "proteins": 4,
            "carbohydrates": 20,
            "fats": 7,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_diabetic_friendly": False,
            "is_low_sodium": True
        },
        {
            "name": "Palomitas de Maíz Caseras",
            "category": SnackCategory.SALTY,
            "description": "Snack bajo en calorías y alto en fibra",
            "recipe": "Ingredientes:\n- 3 cucharadas de maíz para palomitas\n- 1 cucharadita de aceite de coco\n- Sal al gusto (opcional)\n- Especias opcionales (paprika, ajo en polvo)\n\nPreparación:\n1. Calienta el aceite en una olla grande\n2. Agrega el maíz y tapa\n3. Mueve la olla constantemente\n4. Sazona al gusto cuando estén listas",
            "calories": 100,
            "proteins": 3,
            "carbohydrates": 18,
            "fats": 3,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_diabetic_friendly": True,
            "is_low_sodium": True
        },
        {
            "name": "Batido Verde Proteico",
            "category": SnackCategory.PROTEIN,
            "description": "Batido nutritivo post-entrenamiento",
            "recipe": "Ingredientes:\n- 1 taza de espinaca fresca\n- 1 plátano congelado\n- 1 scoop de proteína en polvo\n- 1 taza de leche de almendras\n- 1 cucharada de mantequilla de maní\n- Hielo al gusto\n\nPreparación:\n1. Coloca todos los ingredientes en la licuadora\n2. Licúa hasta obtener consistencia suave\n3. Sirve inmediatamente",
            "calories": 280,
            "proteins": 28,
            "carbohydrates": 30,
            "fats": 8,
            "is_vegetarian": True,
            "is_vegan": False,
            "is_diabetic_friendly": False,
            "is_low_sodium": True
        },
        {
            "name": "Manzana con Mantequilla de Almendras",
            "category": SnackCategory.FRUIT,
            "description": "Simple, delicioso y nutritivo",
            "recipe": "Ingredientes:\n- 1 manzana mediana\n- 2 cucharadas de mantequilla de almendras\n- Canela al gusto (opcional)\n\nPreparación:\n1. Lava y corta la manzana en rodajas\n2. Unta cada rodaja con mantequilla de almendras\n3. Espolvorea canela si deseas\n4. ¡Disfruta!",
            "calories": 220,
            "proteins": 6,
            "carbohydrates": 28,
            "fats": 11,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_diabetic_friendly": True,
            "is_low_sodium": True
        },
        {
            "name": "Rollitos de Jamón y Queso",
            "category": SnackCategory.PROTEIN,
            "description": "Snack alto en proteína, bajo en carbohidratos",
            "recipe": "Ingredientes:\n- 4 lonchas de jamón de pavo bajo en sodio\n- 2 rebanadas de queso bajo en grasa\n- Pepinillos en vinagre\n- Mostaza (opcional)\n\nPreparación:\n1. Extiende las lonchas de jamón\n2. Coloca 1/2 rebanada de queso en cada una\n3. Añade un pepinillo\n4. Enrolla y asegura con palillo\n5. Sirve frío",
            "calories": 120,
            "proteins": 15,
            "carbohydrates": 2,
            "fats": 6,
            "is_vegetarian": False,
            "is_vegan": False,
            "is_diabetic_friendly": True,
            "is_low_sodium": False
        },
        {
            "name": "Edamame con Sal Marina",
            "category": SnackCategory.PROTEIN,
            "description": "Snack oriental rico en proteína vegetal",
            "recipe": "Ingredientes:\n- 1 taza de edamame congelado\n- Sal marina\n- Limón (opcional)\n\nPreparación:\n1. Hierve agua con sal\n2. Cocina el edamame por 5 minutos\n3. Escurre y sirve caliente\n4. Espolvorea sal marina y limón al gusto",
            "calories": 120,
            "proteins": 11,
            "carbohydrates": 10,
            "fats": 5,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_diabetic_friendly": True,
            "is_low_sodium": True
        },
        {
            "name": "Gelatina Proteica con Frutas",
            "category": SnackCategory.SWEET,
            "description": "Postre ligero y refrescante",
            "recipe": "Ingredientes:\n- 1 sobre de gelatina sin azúcar\n- 1 scoop de proteína en polvo (sabor vainilla)\n- 1 taza de frutas mixtas\n- Agua según instrucciones\n\nPreparación:\n1. Prepara la gelatina según instrucciones\n2. Mezcla la proteína en polvo\n3. Añade las frutas cortadas\n4. Refrigera hasta que cuaje\n5. Sirve frío",
            "calories": 150,
            "proteins": 20,
            "carbohydrates": 18,
            "fats": 1,
            "is_vegetarian": True,
            "is_vegan": False,
            "is_diabetic_friendly": True,
            "is_low_sodium": True
        }
    ]
    
    created_snacks = []
    for snack_data in default_snacks:
        existing = db.query(Snack).filter(Snack.name == snack_data["name"]).first()
        if not existing:
            db_snack = Snack(**snack_data)
            db.add(db_snack)
            created_snacks.append(snack_data["name"])
    
    db.commit()
    return {"message": f"Snacks creados: {len(created_snacks)}", "snacks": created_snacks}


