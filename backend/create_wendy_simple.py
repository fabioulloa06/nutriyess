#!/usr/bin/env python3
"""
Script simple para crear usuario administrador directamente en la base de datos
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta

def create_wendy_admin():
    """Crear usuario administrador para Wendy directamente en SQLite"""
    
    print("🔐 Creando Usuario Administrador para Wendy")
    print("=" * 50)
    
    # Datos del administrador
    email = "wendyyessenia01@gmail.com"
    password = "fabioteamo"
    first_name = "Wendy"
    last_name = "Yessenia"
    
    # Hash de la contraseña usando bcrypt
    import bcrypt
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Conectar a la base de datos
    conn = sqlite3.connect('nutriyess.db')
    cursor = conn.cursor()
    
    try:
        # Verificar si el email ya existe
        cursor.execute("SELECT id, email, first_name, last_name FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"❌ El email {email} ya está registrado")
            print(f"👤 Usuario existente: {existing_user[2]} {existing_user[3]}")
            return False
        
        # Crear usuario administrador
        now = datetime.now()
        subscription_end = now + timedelta(days=365*10)  # 10 años
        
        cursor.execute("""
            INSERT INTO users (
                email, password_hash, first_name, last_name, role,
                subscription_status, subscription_plan, is_active, is_verified,
                subscription_start_date, subscription_end_date, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email, password_hash, first_name, last_name, 'admin',
            'active', 'enterprise', 1, 1,
            now.isoformat(), subscription_end.isoformat(), now.isoformat()
        ))
        
        conn.commit()
        
        print("\n✅ ¡Usuario administrador creado exitosamente!")
        print(f"📧 Email: {email}")
        print(f"👤 Nombre: {first_name} {last_name}")
        print(f"🔑 Rol: Administrador")
        print(f"📊 Plan: Enterprise (Ilimitado)")
        print(f"⏰ Suscripción válida hasta: {subscription_end.strftime('%Y-%m-%d')}")
        print(f"\n🌐 Puede acceder a: https://nutriyess-frontend.vercel.app/")
        print(f"🔐 Credenciales:")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    create_wendy_admin()
