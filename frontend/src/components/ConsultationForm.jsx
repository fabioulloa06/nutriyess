import { useState } from 'react'
import { consultationsAPI } from '../api/axios'
import { X, Save, Activity, Ruler, Scale, Scissors } from 'lucide-react'

export default function ConsultationForm({ patientId, patientName, onSuccess, onClose }) {
  const [formData, setFormData] = useState({
    patient_id: patientId,
    weight: '',
    height: '',
    
    // Circumferences
    waist_circumference: '',
    hip_circumference: '',
    arm_circumference: '',
    thigh_circumference: '',
    calf_circumference: '',
    
    // Skinfolds
    triceps_skinfold: '',
    biceps_skinfold: '',
    subscapular_skinfold: '',
    suprailiac_skinfold: '',
    abdominal_skinfold: '',
    
    // Body composition
    body_fat_percentage: '',
    muscle_mass: '',
    
    // Activity level
    activity_level_changed: 0,
    new_activity_level: '',
    
    // Notes
    notes: '',
    recommendations: '',
    diet_plan: '',
    clinical_observations: '',
    follow_up_notes: '',
    next_appointment: ''
  })

  const [activeTab, setActiveTab] = useState('basic')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (checked ? 1 : 0) : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Convertir strings vacíos a null para campos opcionales
      const cleanedData = {}
      for (const [key, value] of Object.entries(formData)) {
        if (value === '' && key !== 'patient_id') {
          cleanedData[key] = null
        } else if (['weight', 'height', 'waist_circumference', 'hip_circumference', 
                    'arm_circumference', 'thigh_circumference', 'calf_circumference',
                    'triceps_skinfold', 'biceps_skinfold', 'subscapular_skinfold',
                    'suprailiac_skinfold', 'abdominal_skinfold', 'body_fat_percentage',
                    'muscle_mass'].includes(key) && value) {
          cleanedData[key] = parseFloat(value)
        } else if (key === 'activity_level_changed') {
          cleanedData[key] = value
        } else {
          cleanedData[key] = value
        }
      }

      await consultationsAPI.create(cleanedData)
      alert('✅ Consulta creada exitosamente')
      onSuccess()
    } catch (error) {
      console.error('Error creating consultation:', error)
      alert('❌ Error al crear consulta: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full my-8">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Nueva Consulta</h2>
            <p className="text-sm text-gray-600">Paciente: {patientName}</p>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={24} />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b overflow-x-auto">
          <button
            onClick={() => setActiveTab('basic')}
            className={`px-6 py-3 font-medium text-sm whitespace-nowrap ${
              activeTab === 'basic'
                ? 'border-b-2 border-green-500 text-green-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Scale size={16} className="inline mr-2" />
            Básico
          </button>
          <button
            onClick={() => setActiveTab('circumferences')}
            className={`px-6 py-3 font-medium text-sm whitespace-nowrap ${
              activeTab === 'circumferences'
                ? 'border-b-2 border-green-500 text-green-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Ruler size={16} className="inline mr-2" />
            Circunferencias
          </button>
          <button
            onClick={() => setActiveTab('skinfolds')}
            className={`px-6 py-3 font-medium text-sm whitespace-nowrap ${
              activeTab === 'skinfolds'
                ? 'border-b-2 border-green-500 text-green-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Scissors size={16} className="inline mr-2" />
            Pliegues
          </button>
          <button
            onClick={() => setActiveTab('activity')}
            className={`px-6 py-3 font-medium text-sm whitespace-nowrap ${
              activeTab === 'activity'
                ? 'border-b-2 border-green-500 text-green-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Activity size={16} className="inline mr-2" />
            Actividad
          </button>
          <button
            onClick={() => setActiveTab('notes')}
            className={`px-6 py-3 font-medium text-sm whitespace-nowrap ${
              activeTab === 'notes'
                ? 'border-b-2 border-green-500 text-green-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            📝 Notas
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {/* Basic Tab */}
          {activeTab === 'basic' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold mb-4">Medidas Básicas</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Peso (kg) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="weight"
                    value={formData.weight}
                    onChange={handleChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Estatura (cm) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="height"
                    value={formData.height}
                    onChange={handleChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    % Grasa Corporal
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="body_fat_percentage"
                    value={formData.body_fat_percentage}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Masa Muscular (kg)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="muscle_mass"
                    value={formData.muscle_mass}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Circumferences Tab */}
          {activeTab === 'circumferences' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold mb-4">Circunferencias (cm)</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Cintura
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="waist_circumference"
                    value={formData.waist_circumference}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Cadera
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="hip_circumference"
                    value={formData.hip_circumference}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Brazo
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="arm_circumference"
                    value={formData.arm_circumference}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Muslo
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="thigh_circumference"
                    value={formData.thigh_circumference}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Pantorrilla
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="calf_circumference"
                    value={formData.calf_circumference}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Skinfolds Tab */}
          {activeTab === 'skinfolds' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold mb-4">Pliegues Cutáneos (mm)</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tríceps
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="triceps_skinfold"
                    value={formData.triceps_skinfold}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Bíceps
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="biceps_skinfold"
                    value={formData.biceps_skinfold}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Subescapular
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="subscapular_skinfold"
                    value={formData.subscapular_skinfold}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Suprailiaco
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="suprailiac_skinfold"
                    value={formData.suprailiac_skinfold}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Abdominal
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    name="abdominal_skinfold"
                    value={formData.abdominal_skinfold}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Activity Tab */}
          {activeTab === 'activity' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold mb-4">Nivel de Actividad Física</h3>
              <div className="mb-4">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="activity_level_changed"
                    checked={formData.activity_level_changed === 1}
                    onChange={handleChange}
                    className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    ¿Cambió el nivel de actividad física?
                  </span>
                </label>
              </div>

              {formData.activity_level_changed === 1 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nuevo Nivel de Actividad
                  </label>
                  <select
                    name="new_activity_level"
                    value={formData.new_activity_level}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  >
                    <option value="">Seleccionar...</option>
                    <option value="sedentario">Sedentario</option>
                    <option value="ligero">Ligero (1-3 días/semana)</option>
                    <option value="moderado">Moderado (3-5 días/semana)</option>
                    <option value="activo">Activo (6-7 días/semana)</option>
                    <option value="muy_activo">Muy Activo (2 veces al día)</option>
                  </select>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Próxima Cita
                </label>
                <input
                  type="datetime-local"
                  name="next_appointment"
                  value={formData.next_appointment}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>
          )}

          {/* Notes Tab */}
          {activeTab === 'notes' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold mb-4">Notas y Observaciones</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Observaciones Clínicas
                </label>
                <textarea
                  name="clinical_observations"
                  value={formData.clinical_observations}
                  onChange={handleChange}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  placeholder="Observaciones durante la consulta..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Recomendaciones
                </label>
                <textarea
                  name="recommendations"
                  value={formData.recommendations}
                  onChange={handleChange}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  placeholder="Recomendaciones nutricionales..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Plan Dietético
                </label>
                <textarea
                  name="diet_plan"
                  value={formData.diet_plan}
                  onChange={handleChange}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  placeholder="Descripción del plan alimenticio..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notas de Seguimiento
                </label>
                <textarea
                  name="follow_up_notes"
                  value={formData.follow_up_notes}
                  onChange={handleChange}
                  rows="2"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  placeholder="Puntos a revisar en próxima consulta..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notas Generales
                </label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleChange}
                  rows="2"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  placeholder="Otras notas..."
                />
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex justify-end space-x-3 mt-6 pt-6 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              <Save size={20} />
              <span>{loading ? 'Guardando...' : 'Guardar Consulta'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

