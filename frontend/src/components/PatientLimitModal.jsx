import { AlertCircle, Users, CreditCard } from 'lucide-react'

function PatientLimitModal({ isOpen, onClose, currentCount, limit }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="flex-shrink-0">
            <AlertCircle className="h-8 w-8 text-orange-500" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Límite de Pacientes Alcanzado
            </h3>
            <p className="text-sm text-gray-600">
              Has alcanzado el límite de tu período de prueba
            </p>
          </div>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-md p-4 mb-4">
          <div className="flex items-center space-x-2 mb-2">
            <Users className="h-5 w-5 text-orange-600" />
            <span className="text-sm font-medium text-orange-800">
              Pacientes actuales: {currentCount}/{limit}
            </span>
          </div>
          <p className="text-sm text-orange-700">
            Tu período de prueba incluye hasta {limit} pacientes. 
            Para agregar más pacientes, necesitas una suscripción activa.
          </p>
        </div>

        <div className="space-y-3">
          <h4 className="font-medium text-gray-900">Planes disponibles:</h4>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
              <div>
                <p className="font-medium text-gray-900">Plan Básico</p>
                <p className="text-sm text-gray-600">Hasta 50 pacientes</p>
              </div>
              <span className="text-lg font-bold text-green-600">$29/mes</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
              <div>
                <p className="font-medium text-gray-900">Plan Profesional</p>
                <p className="text-sm text-gray-600">Hasta 200 pacientes</p>
              </div>
              <span className="text-lg font-bold text-green-600">$79/mes</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
              <div>
                <p className="font-medium text-gray-900">Plan Empresarial</p>
                <p className="text-sm text-gray-600">Pacientes ilimitados</p>
              </div>
              <span className="text-lg font-bold text-green-600">$199/mes</span>
            </div>
          </div>
        </div>

        <div className="flex space-x-3 mt-6">
          <button
            onClick={onClose}
            className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
          >
            Cerrar
          </button>
          <button className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors flex items-center justify-center space-x-2">
            <CreditCard className="h-4 w-4" />
            <span>Suscribirse</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default PatientLimitCard
