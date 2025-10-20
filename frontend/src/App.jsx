import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { Home, Users, BookOpen, Calendar, Coffee, Apple, ClipboardList } from 'lucide-react'

// Pages
import HomePage from './pages/HomePage'
import PatientsPage from './pages/PatientsPage'
import PatientDetailPage from './pages/PatientDetailPage'
import MenusPage from './pages/MenusPage'
import FoodExchangesPage from './pages/FoodExchangesPage'
import SnacksPage from './pages/SnacksPage'
import ConsultationsPage from './pages/ConsultationsPage'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link to="/" className="flex items-center">
                  <Apple className="h-8 w-8 text-primary-600" />
                  <span className="ml-2 text-2xl font-bold text-primary-600">NutriYess</span>
                </Link>
              </div>
              
              <div className="flex items-center space-x-4">
                <NavLink to="/" icon={<Home size={20} />} text="Inicio" />
                <NavLink to="/patients" icon={<Users size={20} />} text="Pacientes" />
                <NavLink to="/menus" icon={<BookOpen size={20} />} text="Menús" />
                <NavLink to="/food-exchanges" icon={<ClipboardList size={20} />} text="Intercambios" />
                <NavLink to="/snacks" icon={<Coffee size={20} />} text="Snacks" />
                <NavLink to="/consultations" icon={<Calendar size={20} />} text="Consultas" />
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/patients" element={<PatientsPage />} />
            <Route path="/patients/:id" element={<PatientDetailPage />} />
            <Route path="/menus" element={<MenusPage />} />
            <Route path="/food-exchanges" element={<FoodExchangesPage />} />
            <Route path="/snacks" element={<SnacksPage />} />
            <Route path="/consultations" element={<ConsultationsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function NavLink({ to, icon, text }) {
  return (
    <Link
      to={to}
      className="flex items-center space-x-1 px-3 py-2 rounded-lg text-gray-700 hover:bg-primary-50 hover:text-primary-600 transition-colors"
    >
      {icon}
      <span className="font-medium">{text}</span>
    </Link>
  )
}

export default App


