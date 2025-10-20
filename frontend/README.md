# NutriYess Frontend

Interfaz de usuario moderna construida con React y TailwindCSS para el sistema de gestión nutricional NutriYess.

## Estructura del Proyecto

```
frontend/
├── index.html              # HTML principal
├── package.json            # Dependencias de Node.js
├── vite.config.js          # Configuración de Vite
├── tailwind.config.js      # Configuración de TailwindCSS
├── postcss.config.js       # Configuración de PostCSS
└── src/
    ├── main.jsx            # Punto de entrada
    ├── App.jsx             # Componente principal
    ├── index.css           # Estilos globales
    ├── api/
    │   └── axios.js        # Configuración de API y funciones
    ├── components/
    │   └── PatientForm.jsx # Formulario de pacientes
    └── pages/
        ├── HomePage.jsx            # Página de inicio
        ├── PatientsPage.jsx        # Lista de pacientes
        ├── PatientDetailPage.jsx   # Detalle de paciente
        ├── MenusPage.jsx           # Menús nutricionales
        ├── FoodExchangesPage.jsx   # Intercambios alimenticios
        ├── SnacksPage.jsx          # Snacks saludables
        └── ConsultationsPage.jsx   # Consultas programadas
```

## Tecnologías

- **React 18** - Biblioteca de UI
- **React Router DOM v6** - Navegación
- **TailwindCSS** - Framework CSS utility-first
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos
- **Vite** - Build tool y dev server
- **date-fns** - Manipulación de fechas

## Instalación

```bash
npm install
```

## Scripts Disponibles

```bash
# Modo desarrollo
npm run dev

# Build para producción
npm run build

# Preview de producción
npm run preview
```

## Componentes Principales

### Navigation
Barra de navegación con enlaces a todas las secciones principales.

### PatientForm
Formulario completo para crear/editar pacientes con validación.

### Páginas

#### HomePage
- Dashboard principal
- Resumen de características
- Accesos rápidos

#### PatientsPage
- Lista de pacientes
- Búsqueda
- Creación de nuevos pacientes

#### PatientDetailPage
- Información completa del paciente
- Tabs: Overview, Cálculos, Consultas
- Cálculos nutricionales automáticos

#### MenusPage
- Menús predefinidos por categoría
- Filtrado
- Vista detallada con información nutricional

#### FoodExchangesPage
- Lista completa de intercambios
- Organizado por categorías
- Tabla con información nutricional

#### SnacksPage
- Recetas de snacks saludables
- Filtros dietéticos
- Vista detallada con preparación

#### ConsultationsPage
- Próximas citas programadas
- Vista de calendario

## Estilos Personalizados

### Clases Utility

```css
.btn-primary     - Botón primario
.btn-secondary   - Botón secundario
.card           - Tarjeta con sombra
.input          - Input estilizado
.label          - Label para formularios
```

### Colores del Tema

```javascript
primary: {
  50: '#f0fdf4',
  100: '#dcfce7',
  200: '#bbf7d0',
  300: '#86efac',
  400: '#4ade80',
  500: '#22c55e',
  600: '#16a34a',
  700: '#15803d',
  800: '#166534',
  900: '#14532d',
}
```

## API Integration

### Configuración Base

```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Módulos API Disponibles

- `patientsAPI` - CRUD de pacientes
- `menusAPI` - Gestión de menús
- `mealPlansAPI` - Planes alimenticios
- `consultationsAPI` - Consultas
- `foodExchangesAPI` - Intercambios alimenticios
- `snacksAPI` - Snacks

## Características de UI/UX

### Responsivo
- Mobile-first design
- Breakpoints: sm, md, lg, xl
- Grid adaptativo

### Interactividad
- Modales para formularios
- Hover states
- Transiciones suaves
- Loading states

### Accesibilidad
- Semántica HTML correcta
- Labels asociados a inputs
- Contraste de colores adecuado
- Navegación por teclado

## Flujo de Usuario

### 1. Gestión de Pacientes
```
Lista → Ver Detalle → Editar
  ↓
Nuevo Paciente → Formulario → Guardar
```

### 2. Consulta
```
Paciente → Nueva Consulta → Cálculos Automáticos → Guardar
```

### 3. Plan Alimenticio
```
Ver Menús → Seleccionar → Ver Intercambios → Crear Plan
```

## Optimizaciones

### Code Splitting
Vite automáticamente divide el código en chunks.

### Lazy Loading
Considera implementar lazy loading para rutas:

```javascript
const HomePage = lazy(() => import('./pages/HomePage'))
```

### Memoización
Usar `useMemo` y `useCallback` para optimizar renders:

```javascript
const calculations = useMemo(() => calculateValues(data), [data])
```

## Deployment

### Build

```bash
npm run build
```

Genera archivos optimizados en `dist/`.

### Netlify

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Vercel

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}
```

### Variables de Entorno

Crear `.env`:

```
VITE_API_URL=https://api.nutriyess.com/api
```

Usar en código:

```javascript
const API_URL = import.meta.env.VITE_API_URL
```

## Testing

### Jest + React Testing Library

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

Ejemplo de test:

```javascript
import { render, screen } from '@testing-library/react'
import HomePage from './pages/HomePage'

test('renders welcome message', () => {
  render(<HomePage />)
  expect(screen.getByText(/Bienvenido a NutriYess/i)).toBeInTheDocument()
})
```

## Mejoras Futuras

- [ ] Autenticación de usuarios
- [ ] Modo oscuro
- [ ] Exportar reportes PDF
- [ ] Gráficos de evolución del paciente
- [ ] Notificaciones push
- [ ] PWA para uso offline
- [ ] Impresión de planes alimenticios
- [ ] Multi-idioma (i18n)

## Troubleshooting

### Error de CORS
Verificar que el backend permita el origen del frontend en la configuración de CORS.

### Error 404 en producción
Configurar redirects para SPA en el servidor de hosting.

### Estilos no cargan
Verificar que PostCSS y TailwindCSS estén correctamente configurados.

## Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/NewFeature`)
3. Commit cambios (`git commit -m 'Add NewFeature'`)
4. Push (`git push origin feature/NewFeature`)
5. Abre un Pull Request

## Licencia

MIT


