from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.menu import Menu, MenuCategory
from pydantic import BaseModel

router = APIRouter()

# Schemas
class MenuCreate(BaseModel):
    name: str
    category: MenuCategory
    description: str | None = None
    calories: float | None = None
    proteins: float | None = None
    carbohydrates: float | None = None
    fats: float | None = None
    fiber: float | None = None
    breakfast: str | None = None
    morning_snack: str | None = None
    lunch: str | None = None
    afternoon_snack: str | None = None
    dinner: str | None = None
    is_custom: bool = False
    supplements: str | None = None

class MenuResponse(BaseModel):
    id: int
    name: str
    category: MenuCategory
    description: str | None
    calories: float | None
    proteins: float | None
    carbohydrates: float | None
    fats: float | None
    fiber: float | None
    breakfast: str | None
    morning_snack: str | None
    lunch: str | None
    afternoon_snack: str | None
    dinner: str | None
    is_custom: bool
    supplements: str | None

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=MenuResponse)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    """Crear un nuevo menú"""
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@router.get("/", response_model=List[MenuResponse])
def get_menus(category: MenuCategory | None = None, db: Session = Depends(get_db)):
    """Obtener lista de menús, opcionalmente filtrados por categoría"""
    query = db.query(Menu)
    if category:
        query = query.filter(Menu.category == category)
    menus = query.all()
    return menus

@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Obtener un menú específico"""
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    return menu

@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: int, menu_data: MenuCreate, db: Session = Depends(get_db)):
    """Actualizar un menú"""
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    
    for key, value in menu_data.model_dump().items():
        setattr(menu, key, value)
    
    db.commit()
    db.refresh(menu)
    return menu

@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Eliminar un menú"""
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    
    db.delete(menu)
    db.commit()
    return {"message": "Menú eliminado exitosamente"}

@router.post("/seed-default-menus")
def seed_default_menus(db: Session = Depends(get_db)):
    """Crear menús de ejemplo predefinidos"""
    default_menus = [
        {
            "name": "Menú Saludable Estándar",
            "category": MenuCategory.HEALTHY,
            "description": "Menú balanceado para personas sanas",
            "calories": 2000,
            "proteins": 100,
            "carbohydrates": 250,
            "fats": 65,
            "fiber": 30,
            "breakfast": "- Avena con frutas y nueces (1 taza)\n- Yogur griego natural (1 porción)\n- Café o té sin azúcar",
            "morning_snack": "- Fruta fresca (1 manzana o pera)\n- Puñado de almendras (10 unidades)",
            "lunch": "- Pechuga de pollo a la plancha (150g)\n- Arroz integral (1 taza)\n- Ensalada verde con vinagreta\n- Agua o jugo natural sin azúcar",
            "afternoon_snack": "- Hummus con vegetales crudos\n- Té verde",
            "dinner": "- Pescado al horno (150g)\n- Verduras salteadas\n- Papa cocida (1 pequeña)\n- Agua"
        },
        {
            "name": "Menú para Diabetes",
            "category": MenuCategory.DIABETES,
            "description": "Menú controlado en carbohidratos y azúcares",
            "calories": 1800,
            "proteins": 110,
            "carbohydrates": 180,
            "fats": 60,
            "fiber": 35,
            "breakfast": "- Huevos revueltos (2 unidades)\n- Pan integral (1 rebanada)\n- Aguacate (1/4)\n- Café sin azúcar",
            "morning_snack": "- Yogur griego sin azúcar\n- Nueces (10 unidades)",
            "lunch": "- Ensalada de atún con vegetales\n- Quinoa (1/2 taza)\n- Brócoli al vapor\n- Agua con limón",
            "afternoon_snack": "- Bastones de apio con mantequilla de maní natural",
            "dinner": "- Pechuga de pavo (150g)\n- Espárragos asados\n- Coliflor al vapor\n- Agua"
        },
        {
            "name": "Menú para Hipertensión",
            "category": MenuCategory.HYPERTENSION,
            "description": "Menú bajo en sodio (Dieta DASH)",
            "calories": 2000,
            "proteins": 100,
            "carbohydrates": 250,
            "fats": 60,
            "fiber": 35,
            "breakfast": "- Avena preparada con leche descremada\n- Plátano en rodajas\n- Jugo de naranja natural",
            "morning_snack": "- Manzana\n- Almendras sin sal (10 unidades)",
            "lunch": "- Salmón al horno con hierbas (sin sal)\n- Arroz integral\n- Espinacas salteadas con ajo\n- Agua",
            "afternoon_snack": "- Yogur bajo en grasa\n- Fresas",
            "dinner": "- Pollo sin piel a la plancha\n- Ensalada variada (sin sal añadida)\n- Batata al horno\n- Agua con pepino"
        },
        {
            "name": "Menú Vegetariano",
            "category": MenuCategory.VEGETARIAN,
            "description": "Menú completo sin carnes",
            "calories": 2000,
            "proteins": 90,
            "carbohydrates": 270,
            "fats": 65,
            "fiber": 40,
            "breakfast": "- Tostadas integrales con aguacate\n- Tofu revuelto con vegetales\n- Jugo verde natural",
            "morning_snack": "- Batido de proteína vegetal con frutas",
            "lunch": "- Lentejas guisadas\n- Arroz integral\n- Ensalada de col con zanahoria\n- Agua de Jamaica sin azúcar",
            "afternoon_snack": "- Hummus con pan pita integral",
            "dinner": "- Hamburguesa de garbanzos\n- Ensalada mixta\n- Batata rostizada\n- Té de hierbas"
        },
        {
            "name": "Menú Vegano",
            "category": MenuCategory.VEGAN,
            "description": "Menú 100% vegetal",
            "calories": 2000,
            "proteins": 85,
            "carbohydrates": 280,
            "fats": 65,
            "fiber": 45,
            "breakfast": "- Avena con leche de almendras\n- Semillas de chía\n- Frutas del bosque\n- Mantequilla de maní",
            "morning_snack": "- Batido verde (espinaca, plátano, leche vegetal)",
            "lunch": "- Bowl de quinoa con frijoles negros\n- Aguacate\n- Pico de gallo\n- Agua",
            "afternoon_snack": "- Mix de frutos secos y semillas",
            "dinner": "- Tempeh marinado\n- Vegetales salteados\n- Arroz salvaje\n- Té verde"
        },
        {
            "name": "Menú para Deportistas",
            "category": MenuCategory.ATHLETE,
            "description": "Menú alto en proteínas y energía",
            "calories": 2800,
            "proteins": 160,
            "carbohydrates": 350,
            "fats": 80,
            "fiber": 35,
            "breakfast": "- Claras de huevo (4) con 1 huevo entero\n- Avena con plátano y miel\n- Jugo de naranja",
            "morning_snack": "- Batido de proteína con frutas\n- Almendras",
            "lunch": "- Pechuga de pollo (200g)\n- Arroz integral (1.5 tazas)\n- Ensalada grande\n- Batata\n- Agua",
            "afternoon_snack": "- Sándwich de atún con pan integral\n- Fruta",
            "dinner": "- Carne magra o pescado (200g)\n- Quinoa\n- Verduras variadas\n- Agua",
            "supplements": "- Proteína Whey post-entrenamiento\n- BCAA durante entrenamiento\n- Creatina monohidrato (5g)\n- Multivitamínico"
        }
    ]
    
    created_menus = []
    for menu_data in default_menus:
        existing = db.query(Menu).filter(Menu.name == menu_data["name"]).first()
        if not existing:
            db_menu = Menu(**menu_data)
            db.add(db_menu)
            created_menus.append(menu_data["name"])
    
    db.commit()
    return {"message": f"Menús creados: {len(created_menus)}", "menus": created_menus}


