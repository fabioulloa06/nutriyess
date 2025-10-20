import { useAuth } from '../contexts/AuthContext'
import { Users, Clock, AlertCircle } from 'lucide-react'

function PatientLimitCard() {
  const { subscription, getDaysRemaining, getPatientLimit } = useAuth()
  
  const daysRemaining = getDaysRemaining()
  const patientLimit = getPatientLimit()
  const isTrial = subscription?.status === 'trial'

  if (!isTrial) {
    return null // No mostrar para suscripciones pagas
  }

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 mb-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <Users className="h-8 w-8 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-medium text-blue-900">
              Período de Prueba
            </h3>
            <p className="text-sm text-blue-700">
              Límite: {patientLimit} pacientes
            </p>
          </div>
        </div>
        
        <div className="text-right">
          <div className="flex items-center space-x-2 text-sm text-blue-700">
            <Clock className="h-4 w-4" />
            <span>{daysRemaining} días restantes</span>
          </div>
          
          {daysRemaining <= 7 && (
            <div className="mt-2 flex items-center space-x-1 text-orange-600">
              <AlertCircle className="h-4 w-4" />
              <span className="text-xs font-medium">Próximo a expirar</span>
            </div>
          )}
        </div>
      </div>
      
      {daysRemaining <= 7 && (
        <div className="mt-3 pt-3 border-t border-blue-200">
          <div className="flex items-center justify-between">
            <p className="text-sm text-blue-700">
              Tu período de prueba expira pronto. Suscríbete para continuar.
            </p>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
              Suscribirse
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default PatientLimitCard
