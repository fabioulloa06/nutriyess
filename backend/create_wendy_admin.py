#!/usr/bin/env python3
"""
Script para crear automáticamente el usuario administrador de Wendy
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db, engine
from models.user import User, UserRole, SubscriptionStatus, SubscriptionPlan
from utils.auth import get_password_hash

def create_wendy_admin():
    """Crear usuario administrador para Wendy"""
    
    print("🔐 Creando Usuario Administrador para Wendy")
    print("=" * 50)
    
    # Datos del administrador
    email = "wendyyessenia01@gmail.com"
    password = "fabioteamo"
    first_name = "Wendy"
    last_name = "Yessenia"
    
    # Crear sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar si el email ya existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ El email {email} ya está registrado")
            print(f"👤 Usuario existente: {existing_user.first_name} {existing_user.last_name}")
            print(f"🔑 Rol: {existing_user.role}")
            return False
        
        # Crear usuario administrador
        admin_user = User(
            email=email,
            password_hash=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            role=UserRole.admin,
            subscription_status=SubscriptionStatus.active,
            subscription_plan=SubscriptionPlan.enterprise,
            is_active=True,
            is_verified=True,
            subscription_start_date=datetime.now(),
            subscription_end_date=datetime.now() + timedelta(days=365*10)  # 10 años
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("\n✅ ¡Usuario administrador creado exitosamente!")
        print(f"📧 Email: {email}")
        print(f"👤 Nombre: {first_name} {last_name}")
        print(f"🔑 Rol: Administrador")
        print(f"📊 Plan: Enterprise (Ilimitado)")
        print(f"⏰ Suscripción válida hasta: {admin_user.subscription_end_date.strftime('%Y-%m-%d')}")
        print(f"\n🌐 Puede acceder a: https://nutriyess-frontend.vercel.app/")
        print(f"🔐 Credenciales:")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    create_wendy_admin()
