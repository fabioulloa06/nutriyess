# 🐳 NutriYess - Docker Setup

## 🚀 Inicio Rápido

### Windows:
```bash
start-docker.bat
```

### Linux/Mac:
```bash
chmod +x start-docker.sh
./start-docker.sh
```

### Manual:
```bash
# Construir y ejecutar
docker-compose up --build

# En segundo plano
docker-compose up -d --build
```

## 📋 Servicios

| Servicio | Puerto | URL | Descripción |
|----------|--------|-----|-------------|
| Frontend | 3000 | http://localhost:3000 | React + Vite |
| Backend | 8000 | http://localhost:8000 | FastAPI |
| Database | 5432 | localhost:5432 | PostgreSQL |

## 🔧 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir un servicio
docker-compose build backend
docker-compose up -d backend

# Ejecutar comandos en contenedores
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec db psql -U nutriyess -d nutriyess
```

## 🗄️ Base de Datos

- **Usuario**: nutriyess
- **Contraseña**: nutriyess123
- **Base de datos**: nutriyess
- **Puerto**: 5432

### Conectar desde fuera de Docker:
```bash
psql -h localhost -p 5432 -U nutriyess -d nutriyess
```

## 🐛 Debugging

### Verificar que los servicios estén funcionando:
```bash
# Health check del backend
curl http://localhost:8000/health

# Verificar frontend
curl http://localhost:3000
```

### Reiniciar un servicio específico:
```bash
docker-compose restart backend
docker-compose restart frontend
```

## 📦 Despliegue en Producción

### Para desplegar en cualquier servidor:

1. **Copiar archivos**:
   ```bash
   # Copiar estos archivos al servidor:
   - docker-compose.yml
   - backend/Dockerfile
   - frontend/Dockerfile
   - backend/ (directorio completo)
   - frontend/ (directorio completo)
   ```

2. **Configurar variables de entorno**:
   ```bash
   # Editar docker-compose.yml y cambiar:
   - DATABASE_URL
   - JWT_SECRET_KEY
   - VITE_API_URL
   ```

3. **Ejecutar**:
   ```bash
   docker-compose up -d --build
   ```

## 🔒 Seguridad

### Para producción, cambiar:
- Contraseñas de base de datos
- JWT_SECRET_KEY
- Configurar firewall
- Usar HTTPS
- Configurar dominio personalizado

## 📊 Monitoreo

```bash
# Ver uso de recursos
docker stats

# Ver estado de contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f
```
