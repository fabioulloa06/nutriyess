import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom'
import { Home, Users, BookOpen, Calendar, Coffee, Apple, ClipboardList, LogOut } from 'lucide-react'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'

// Pages
import HomePage from './pages/HomePage'
import PatientsPage from './pages/PatientsPage'
import PatientDetailPage from './pages/PatientDetailPage'
import MenusPage from './pages/MenusPage'
import FoodExchangesPage from './pages/FoodExchangesPage'
import SnacksPage from './pages/SnacksPage'
import ConsultationsPage from './pages/ConsultationsPage'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'

function AppContent() {
  const { user, logout, isAuthenticated } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="flex items-center">
                <Apple className="h-8 w-8 text-green-600" />
                <span className="ml-2 text-2xl font-bold text-green-600">NutriYess</span>
              </Link>
            </div>
            
            {isAuthenticated() && (
              <div className="flex items-center space-x-4">
                <NavLink to="/" icon={<Home size={20} />} text="Inicio" />
                <NavLink to="/patients" icon={<Users size={20} />} text="Pacientes" />
                <NavLink to="/menus" icon={<BookOpen size={20} />} text="Menús" />
                <NavLink to="/food-exchanges" icon={<ClipboardList size={20} />} text="Intercambios" />
                <NavLink to="/snacks" icon={<Coffee size={20} />} text="Snacks" />
                <NavLink to="/consultations" icon={<Calendar size={20} />} text="Consultas" />
                
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">{user?.email}</span>
                  <button
                    onClick={logout}
                    className="flex items-center space-x-1 text-red-600 hover:text-red-700"
                  >
                    <LogOut size={16} />
                    <span>Salir</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/" element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          } />
          <Route path="/patients" element={
            <ProtectedRoute>
              <PatientsPage />
            </ProtectedRoute>
          } />
          <Route path="/patients/:id" element={
            <ProtectedRoute>
              <PatientDetailPage />
            </ProtectedRoute>
          } />
          <Route path="/menus" element={
            <ProtectedRoute>
              <MenusPage />
            </ProtectedRoute>
          } />
          <Route path="/food-exchanges" element={
            <ProtectedRoute>
              <FoodExchangesPage />
            </ProtectedRoute>
          } />
          <Route path="/snacks" element={
            <ProtectedRoute>
              <SnacksPage />
            </ProtectedRoute>
          } />
          <Route path="/consultations" element={
            <ProtectedRoute>
              <ConsultationsPage />
            </ProtectedRoute>
          } />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
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


