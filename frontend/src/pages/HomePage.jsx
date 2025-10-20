import { Link } from 'react-router-dom'
import { Users, BookOpen, ClipboardList, Coffee, TrendingUp, Calendar } from 'lucide-react'

function HomePage() {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl p-8 text-white">
        <h1 className="text-4xl font-bold mb-4">Bienvenido a NutriYess</h1>
        <p className="text-xl text-primary-50">
          Sistema integral de gestión nutricional para profesionales de la salud
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Gestión de Pacientes"
          description="Registro completo de datos antropométricos e historial clínico"
          icon={<Users size={40} />}
          color="bg-blue-500"
        />
        <StatCard
          title="Cálculos Automáticos"
          description="IMC, peso ideal, requerimiento calórico y más"
          icon={<TrendingUp size={40} />}
          color="bg-green-500"
        />
        <StatCard
          title="Seguimiento"
          description="Historial de consultas y evolución de pacientes"
          icon={<Calendar size={40} />}
          color="bg-purple-500"
        />
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <FeatureCard
          to="/patients"
          icon={<Users size={32} />}
          title="Pacientes"
          description="Administra la información completa de tus pacientes"
          color="text-blue-600"
        />
        <FeatureCard
          to="/menus"
          icon={<BookOpen size={32} />}
          title="Menús"
          description="Menús predefinidos para diferentes condiciones"
          color="text-green-600"
        />
        <FeatureCard
          to="/food-exchanges"
          icon={<ClipboardList size={32} />}
          title="Intercambios"
          description="Lista completa de intercambios alimenticios"
          color="text-orange-600"
        />
        <FeatureCard
          to="/snacks"
          icon={<Coffee size={32} />}
          title="Snacks Saludables"
          description="Recetas nutritivas y deliciosas"
          color="text-pink-600"
        />
        <FeatureCard
          to="/consultations"
          icon={<Calendar size={32} />}
          title="Consultas"
          description="Historial y seguimiento de consultas"
          color="text-indigo-600"
        />
      </div>

      {/* Features List */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Características Principales</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FeatureItem text="Cálculo de requerimiento calórico para diferentes tipos de pacientes" />
          <FeatureItem text="Fórmulas especializadas para hospitalización, UCI, deportistas" />
          <FeatureItem text="Menús para diabetes, hipertensión, distensión abdominal" />
          <FeatureItem text="Planes vegetarianos, veganos y para deportistas" />
          <FeatureItem text="Sistema de intercambios alimenticios completo" />
          <FeatureItem text="Recomendaciones de suplementos del mercado colombiano" />
          <FeatureItem text="Base de datos de snacks saludables y creativos" />
          <FeatureItem text="Historial completo de consultas y seguimiento" />
          <FeatureItem text="Cálculo de IMC según rango de edad" />
          <FeatureItem text="Peso saludable y peso ajustado automático" />
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, description, icon, color }) {
  return (
    <div className="card">
      <div className={`${color} w-16 h-16 rounded-lg flex items-center justify-center text-white mb-4`}>
        {icon}
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function FeatureCard({ to, icon, title, description, color }) {
  return (
    <Link to={to} className="card hover:shadow-lg transition-shadow">
      <div className={`${color} mb-4`}>{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </Link>
  )
}

function FeatureItem({ text }) {
  return (
    <div className="flex items-start space-x-2">
      <div className="w-2 h-2 bg-primary-600 rounded-full mt-2"></div>
      <p className="text-gray-700">{text}</p>
    </div>
  )
}

export default HomePage


