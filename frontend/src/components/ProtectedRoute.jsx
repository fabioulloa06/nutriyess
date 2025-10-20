import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Clock, AlertTriangle } from 'lucide-react'

function ProtectedRoute({ children }) {
  const { isAuthenticated, isSubscriptionActive, getDaysRemaining, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-500"></div>
      </div>
    )
  }

  if (!isAuthenticated()) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  // Check subscription status
  if (!isSubscriptionActive()) {
    const daysRemaining = getDaysRemaining()
    
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100">
              <Clock className="h-6 w-6 text-yellow-600" />
            </div>
            <h2 className="mt-4 text-xl font-semibold text-gray-900">
              Período de Prueba
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              {daysRemaining > 0 
                ? `Te quedan ${daysRemaining} días de prueba gratuita`
                : 'Tu período de prueba ha expirado'
              }
            </p>
            
            {daysRemaining > 0 ? (
              <div className="mt-4">
                <p className="text-sm text-gray-500 mb-4">
                  Disfruta de todas las funciones de NutriYess durante tu período de prueba.
                  <br />
                  <strong>Límite: 3 pacientes</strong>
                </p>
                <button
                  onClick={() => window.location.reload()}
                  className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
                >
                  Continuar
                </button>
              </div>
            ) : (
              <div className="mt-4">
                <div className="bg-red-50 border border-red-200 rounded-md p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <AlertTriangle className="h-5 w-5 text-red-400" />
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">
                        Suscripción Requerida
                      </h3>
                      <div className="mt-2 text-sm text-red-700">
                        <p>Tu período de prueba ha expirado. Para continuar usando NutriYess, necesitas una suscripción activa.</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 space-y-2">
                  <button className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors">
                    Suscribirse Ahora
                  </button>
                  <button 
                    onClick={() => window.location.href = '/logout'}
                    className="w-full bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
                  >
                    Cerrar Sesión
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  return children
}

export default ProtectedRoute
