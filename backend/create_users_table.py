import sqlite3
import bcrypt
from datetime import datetime, timedelta

def create_users_table():
    """Crear tabla users manualmente"""
    
    conn = sqlite3.connect('nutriyess.db')
    cursor = conn.cursor()
    
    try:
        # Crear tabla users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR UNIQUE NOT NULL,
                password_hash VARCHAR NOT NULL,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                phone VARCHAR,
                role VARCHAR DEFAULT 'nutricionista',
                subscription_status VARCHAR DEFAULT 'trial',
                subscription_plan VARCHAR DEFAULT 'basic',
                trial_start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                trial_end_date DATETIME,
                subscription_start_date DATETIME,
                subscription_end_date DATETIME,
                professional_license VARCHAR,
                specialization VARCHAR,
                clinic_name VARCHAR,
                clinic_address TEXT,
                bio TEXT,
                is_active BOOLEAN DEFAULT 1,
                is_verified BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        
        conn.commit()
        print("✅ Tabla 'users' creada exitosamente")
        
        # Verificar que existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        if result:
            print("✅ Tabla 'users' verificada")
        else:
            print("❌ Error: Tabla 'users' no encontrada")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_users_table()
