#!/usr/bin/env python3
"""
Script para crear un usuario administrador con acceso ilimitado
Uso: python create_admin.py
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db, engine
from models.user import User, UserRole, SubscriptionStatus, SubscriptionPlan
from utils.auth import get_password_hash

def create_admin_user():
    """Crear un usuario administrador"""
    
    # Solicitar datos del administrador
    print("🔐 Creando Usuario Administrador")
    print("=" * 40)
    
    email = input("📧 Email del administrador: ").strip()
    if not email:
        print("❌ Email es requerido")
        return False
    
    password = input("🔑 Contraseña (mínimo 6 caracteres): ").strip()
    if len(password) < 6:
        print("❌ La contraseña debe tener al menos 6 caracteres")
        return False
    
    first_name = input("👤 Nombre: ").strip()
    if not first_name:
        print("❌ Nombre es requerido")
        return False
    
    last_name = input("👤 Apellido: ").strip()
    if not last_name:
        print("❌ Apellido es requerido")
        return False
    
    phone = input("📱 Teléfono (opcional): ").strip()
    professional_license = input("📋 Licencia profesional (opcional): ").strip()
    clinic_name = input("🏥 Nombre de la clínica (opcional): ").strip()
    
    # Crear sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar si el email ya existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ El email {email} ya está registrado")
            return False
        
        # Crear usuario administrador
        admin_user = User(
            email=email,
            password_hash=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=UserRole.admin,
            subscription_status=SubscriptionStatus.active,
            subscription_plan=SubscriptionPlan.enterprise,
            professional_license=professional_license,
            clinic_name=clinic_name,
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
        print("\n🌐 Puede acceder a: https://nutriyess-frontend.vercel.app/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def list_admin_users():
    """Listar usuarios administradores existentes"""
    db = next(get_db())
    
    try:
        admins = db.query(User).filter(User.role == UserRole.admin).all()
        
        if not admins:
            print("📋 No hay usuarios administradores registrados")
            return
        
        print("\n👑 Usuarios Administradores:")
        print("=" * 50)
        
        for admin in admins:
            status = "✅ Activo" if admin.is_active else "❌ Inactivo"
            verified = "✅ Verificado" if admin.is_verified else "⏳ Pendiente"
            
            print(f"📧 Email: {admin.email}")
            print(f"👤 Nombre: {admin.first_name} {admin.last_name}")
            print(f"📊 Plan: {admin.subscription_plan.value}")
            print(f"🔑 Estado: {status}")
            print(f"✅ Verificación: {verified}")
            print(f"📅 Creado: {admin.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error al listar usuarios: {str(e)}")
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 NutriYess - Gestión de Administradores")
    print("=" * 50)
    
    while True:
        print("\n📋 Opciones disponibles:")
        print("1. Crear nuevo usuario administrador")
        print("2. Listar usuarios administradores")
        print("3. Salir")
        
        choice = input("\n🔢 Selecciona una opción (1-3): ").strip()
        
        if choice == "1":
            create_admin_user()
        elif choice == "2":
            list_admin_users()
        elif choice == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Por favor selecciona 1, 2 o 3.")

if __name__ == "__main__":
    main()
