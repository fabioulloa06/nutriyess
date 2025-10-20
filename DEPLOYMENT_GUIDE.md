# Guía de Despliegue en Producción
# ================================

## 🌐 Arquitectura Final

### Frontend (Vercel)
- URL: https://nutriyess-frontend.vercel.app/
- Costo: GRATIS
- Características: CDN global, SSL automático, despliegue desde GitHub

### Backend (Tu Servidor/VPS)
- URL: https://tu-dominio.com/api
- Costo: $5-20/mes (dependiendo del proveedor)
- Características: Control total, PostgreSQL incluida, escalable

## 🚀 Opciones de Servidor

### 1. DigitalOcean Droplet
```bash
# Droplet básico: $6/mes
# 1GB RAM, 1 CPU, 25GB SSD
# Ubuntu 22.04 LTS
```

### 2. AWS EC2
```bash
# t3.micro: $8.50/mes (primer año gratis)
# 1GB RAM, 1 CPU, 8GB SSD
```

### 3. Google Cloud Platform
```bash
# e2-micro: $6/mes
# 1GB RAM, 1 CPU, 10GB SSD
```

### 4. Vultr
```bash
# Cloud Compute: $6/mes
# 1GB RAM, 1 CPU, 25GB SSD
```

## 📋 Pasos para Despliegue

### 1. Crear Servidor
```bash
# Crear droplet/servidor con Ubuntu 22.04
# Configurar SSH key
# Actualizar sistema
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Docker
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt install docker-compose-plugin -y

# Agregar usuario a grupo docker
sudo usermod -aG docker $USER
```

### 3. Configurar Dominio (Opcional)
```bash
# Comprar dominio (ej: nutriyess.com)
# Configurar DNS A record apuntando a tu servidor
# Configurar SSL con Let's Encrypt
```

### 4. Desplegar Aplicación
```bash
# Clonar repositorio
git clone https://github.com/fabioulloa06/nutriyess.git
cd nutriyess

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Iniciar servicios
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Configurar Vercel
```bash
# En Vercel, agregar variable de entorno:
VITE_API_URL = https://tu-dominio.com/api
```

## 🔒 Seguridad

### Variables de Entorno (.env)
```bash
# Base de datos
DB_PASSWORD=tu-password-super-seguro

# JWT
JWT_SECRET_KEY=tu-jwt-secret-muy-largo-y-seguro

# Dominio
DOMAIN=tu-dominio.com
```

### Firewall
```bash
# Configurar UFW
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 📊 Monitoreo

### Logs
```bash
# Ver logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f

# Logs específicos
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Backup de Base de Datos
```bash
# Backup automático (cron job)
0 2 * * * docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U nutriyess nutriyess > backup_$(date +\%Y\%m\%d).sql
```

## 💰 Costos Estimados

### Opción Económica (Recomendada)
- **Servidor**: $6/mes (DigitalOcean)
- **Dominio**: $12/año (opcional)
- **SSL**: GRATIS (Let's Encrypt)
- **Frontend**: GRATIS (Vercel)
- **Total**: ~$7/mes

### Opción Profesional
- **Servidor**: $20/mes (más recursos)
- **Dominio**: $12/año
- **CDN**: $5/mes (CloudFlare)
- **Monitoreo**: $10/mes (opcional)
- **Total**: ~$35/mes

## 🎯 Ventajas de esta Arquitectura

✅ **Frontend en Vercel**: CDN global, SSL automático, despliegue automático
✅ **Backend en Docker**: Control total, escalable, profesional
✅ **Base de datos incluida**: PostgreSQL en el mismo servidor
✅ **Costo predecible**: Sin sorpresas de Railway
✅ **Escalable**: Puedes agregar más recursos cuando necesites
✅ **Profesional**: Arquitectura de producción real

## 🚀 Próximos Pasos

1. **Elegir proveedor** de servidor
2. **Crear servidor** y configurar Docker
3. **Desplegar backend** con docker-compose
4. **Configurar dominio** y SSL
5. **Actualizar Vercel** con nueva URL del backend
6. **¡Listo para producción!**