import { useState, useEffect } from 'react'
import { Calendar, Clock } from 'lucide-react'
import { consultationsAPI } from '../api/axios'

function ConsultationsPage() {
  const [consultations, setConsultations] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUpcomingConsultations()
  }, [])

  const loadUpcomingConsultations = async () => {
    try {
      const response = await consultationsAPI.getUpcoming()
      setConsultations(response.data)
    } catch (error) {
      console.error('Error loading consultations:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Cargando consultas...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <h1 className="text-3xl font-bold text-gray-900">Próximas Consultas</h1>

      {/* Description */}
      <div className="card bg-primary-50 border-l-4 border-primary-600">
        <p className="text-gray-700">
          Mantén un registro organizado de todas tus consultas programadas. 
          Para ver el historial completo de un paciente, visita su perfil individual.
        </p>
      </div>

      {/* Upcoming Consultations */}
      {consultations.length === 0 ? (
        <div className="card text-center py-12">
          <Calendar className="mx-auto text-gray-400 mb-4" size={64} />
          <p className="text-gray-600 text-lg">No hay consultas próximas programadas</p>
          <p className="text-gray-500">Las citas programadas aparecerán aquí</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {consultations.map((consultation) => (
            <div key={consultation.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                    <Calendar className="text-primary-600" size={24} />
                  </div>
                  <div>
                    <p className="font-semibold text-lg">
                      {consultation.patient?.first_name} {consultation.patient?.last_name}
                    </p>
                    <p className="text-sm text-gray-600">{consultation.patient?.identification}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center space-x-2 text-gray-700">
                  <Calendar size={16} className="text-primary-600" />
                  <span className="text-sm font-medium">
                    {formatDate(consultation.next_appointment)}
                  </span>
                </div>
                
                <div className="flex items-center space-x-2 text-gray-700">
                  <Clock size={16} className="text-primary-600" />
                  <span className="text-sm font-medium">
                    {formatTime(consultation.next_appointment)}
                  </span>
                </div>

                {consultation.notes && (
                  <div className="pt-3 border-t">
                    <p className="text-sm text-gray-600 line-clamp-2">{consultation.notes}</p>
                  </div>
                )}
              </div>

              <div className="mt-4 pt-4 border-t">
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div>
                    <p className="text-xs text-gray-600">Peso</p>
                    <p className="font-medium">{consultation.weight} kg</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">IMC</p>
                    <p className="font-medium">{consultation.bmi?.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Calorías</p>
                    <p className="font-medium">{consultation.caloric_requirement?.toFixed(0)}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Info Section */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Gestión de Consultas</h2>
        <div className="space-y-3 text-gray-700">
          <p>• Para agregar una nueva consulta, ve al perfil del paciente</p>
          <p>• Cada consulta registra automáticamente peso, IMC y requerimientos calóricos</p>
          <p>• Puedes programar la próxima cita y agregar notas y recomendaciones</p>
          <p>• El historial completo se guarda en el perfil de cada paciente</p>
        </div>
      </div>
    </div>
  )
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('es-CO', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function formatTime(dateString) {
  return new Date(dateString).toLocaleTimeString('es-CO', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

export default ConsultationsPage


