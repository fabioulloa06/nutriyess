import { useState } from 'react'
import { patientsAPI } from '../api/axios'
import { Scale, Ruler, Scissors, Activity } from 'lucide-react'

function PatientForm({ patient = null, onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    first_name: patient?.first_name || '',
    last_name: patient?.last_name || '',
    identification: patient?.identification || '',
    birth_date: patient?.birth_date || '',
    gender: patient?.gender || 'masculino',
    weight: patient?.weight || '',
    height: patient?.height || '',
    
    // Datos antropométricos completos
    body_fat_percentage: patient?.body_fat_percentage || '',
    muscle_mass: patient?.muscle_mass || '',
    waist_circumference: patient?.waist_circumference || '',
    hip_circumference: patient?.hip_circumference || '',
    arm_circumference: patient?.arm_circumference || '',
    thigh_circumference: patient?.thigh_circumference || '',
    calf_circumference: patient?.calf_circumference || '',
    triceps_skinfold: patient?.triceps_skinfold || '',
    biceps_skinfold: patient?.biceps_skinfold || '',
    subscapular_skinfold: patient?.subscapular_skinfold || '',
    suprailiac_skinfold: patient?.suprailiac_skinfold || '',
    abdominal_skinfold: patient?.abdominal_skinfold || '',
    
    medical_history: patient?.medical_history || '',
    nutritional_history: patient?.nutritional_history || '',
    allergies: patient?.allergies || '',
    medications: patient?.medications || '',
    patient_type: patient?.patient_type || 'sano',
    activity_level: patient?.activity_level || 'moderado',
    is_vegetarian: patient?.is_vegetarian || 0,
    has_diabetes: patient?.has_diabetes || 0,
    has_hypertension: patient?.has_hypertension || 0,
    has_bloating: patient?.has_bloating || 0,
    other_conditions: patient?.other_conditions || '',
  })

  const [activeTab, setActiveTab] = useState('personal')

  const [error, setError] = useState('')
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
    setError('')

    try {
      if (patient) {
        await patientsAPI.update(patient.id, formData)
      } else {
        await patientsAPI.create(formData)
      }
      onSuccess()
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al guardar el paciente')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Tabs */}
      <div className="flex space-x-4 border-b overflow-x-auto">
        <button
          type="button"
          onClick={() => setActiveTab('personal')}
          className={`px-4 py-2 font-medium text-sm whitespace-nowrap border-b-2 transition-colors ${
            activeTab === 'personal'
              ? 'border-green-500 text-green-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          👤 Personal
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('basic')}
          className={`px-4 py-2 font-medium text-sm whitespace-nowrap border-b-2 transition-colors ${
            activeTab === 'basic'
              ? 'border-green-500 text-green-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          <Scale size={16} className="inline mr-1" />
          Básico
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('circumferences')}
          className={`px-4 py-2 font-medium text-sm whitespace-nowrap border-b-2 transition-colors ${
            activeTab === 'circumferences'
              ? 'border-green-500 text-green-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          <Ruler size={16} className="inline mr-1" />
          Circunferencias
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('skinfolds')}
          className={`px-4 py-2 font-medium text-sm whitespace-nowrap border-b-2 transition-colors ${
            activeTab === 'skinfolds'
              ? 'border-green-500 text-green-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          <Scissors size={16} className="inline mr-1" />
          Pliegues
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('medical')}
          className={`px-4 py-2 font-medium text-sm whitespace-nowrap border-b-2 transition-colors ${
            activeTab === 'medical'
              ? 'border-green-500 text-green-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          🏥 Médico
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Personal Information Tab */}
        {activeTab === 'personal' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Información Personal</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Nombres</label>
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Apellidos</label>
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Identificación</label>
                <input
                  type="text"
                  name="identification"
                  value={formData.identification}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Fecha de Nacimiento</label>
                <input
                  type="date"
                  name="birth_date"
                  value={formData.birth_date}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Género</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="input"
                  required
                >
                  <option value="masculino">Masculino</option>
                  <option value="femenino">Femenino</option>
                  <option value="otro">Otro</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Basic Anthropometric Data Tab */}
        {activeTab === 'basic' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Medidas Básicas</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Peso (kg) *</label>
                <input
                  type="number"
                  step="0.1"
                  name="weight"
                  value={formData.weight}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Altura (cm) *</label>
                <input
                  type="number"
                  step="0.1"
                  name="height"
                  value={formData.height}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">% Grasa Corporal</label>
                <input
                  type="number"
                  step="0.1"
                  name="body_fat_percentage"
                  value={formData.body_fat_percentage}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Masa Muscular (kg)</label>
                <input
                  type="number"
                  step="0.1"
                  name="muscle_mass"
                  value={formData.muscle_mass}
                  onChange={handleChange}
                  className="input"
                />
              </div>
            </div>
          </div>
        )}

        {/* Circumferences Tab */}
        {activeTab === 'circumferences' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Circunferencias (cm)</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Cintura</label>
                <input
                  type="number"
                  step="0.1"
                  name="waist_circumference"
                  value={formData.waist_circumference}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Cadera</label>
                <input
                  type="number"
                  step="0.1"
                  name="hip_circumference"
                  value={formData.hip_circumference}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Brazo</label>
                <input
                  type="number"
                  step="0.1"
                  name="arm_circumference"
                  value={formData.arm_circumference}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Muslo</label>
                <input
                  type="number"
                  step="0.1"
                  name="thigh_circumference"
                  value={formData.thigh_circumference}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Pantorrilla</label>
                <input
                  type="number"
                  step="0.1"
                  name="calf_circumference"
                  value={formData.calf_circumference}
                  onChange={handleChange}
                  className="input"
                />
              </div>
            </div>
          </div>
        )}

        {/* Skinfolds Tab */}
        {activeTab === 'skinfolds' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Pliegues Cutáneos (mm)</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="label">Tríceps</label>
                <input
                  type="number"
                  step="0.1"
                  name="triceps_skinfold"
                  value={formData.triceps_skinfold}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Bíceps</label>
                <input
                  type="number"
                  step="0.1"
                  name="biceps_skinfold"
                  value={formData.biceps_skinfold}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Subescapular</label>
                <input
                  type="number"
                  step="0.1"
                  name="subscapular_skinfold"
                  value={formData.subscapular_skinfold}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Suprailiaco</label>
                <input
                  type="number"
                  step="0.1"
                  name="suprailiac_skinfold"
                  value={formData.suprailiac_skinfold}
                  onChange={handleChange}
                  className="input"
                />
              </div>
              <div>
                <label className="label">Abdominal</label>
                <input
                  type="number"
                  step="0.1"
                  name="abdominal_skinfold"
                  value={formData.abdominal_skinfold}
                  onChange={handleChange}
                  className="input"
                />
              </div>
            </div>
          </div>
        )}

        {/* Medical Information Tab */}
        {activeTab === 'medical' && (
          <div className="space-y-6">
            {/* Patient Type and Activity */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Tipo de Paciente y Actividad</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label">Tipo de Paciente</label>
                  <select
                    name="patient_type"
                    value={formData.patient_type}
                    onChange={handleChange}
                    className="input"
                  >
                    <option value="sano">Sano</option>
                    <option value="hospitalizado">Hospitalizado</option>
                    <option value="uci">UCI</option>
                    <option value="deportista">Deportista</option>
                    <option value="adolescente">Adolescente</option>
                    <option value="adulto_mayor">Adulto Mayor</option>
                    <option value="embarazada">Embarazada</option>
                  </select>
                </div>
                <div>
                  <label className="label">Nivel de Actividad</label>
                  <select
                    name="activity_level"
                    value={formData.activity_level}
                    onChange={handleChange}
                    className="input"
                  >
                    <option value="sedentario">Sedentario</option>
                    <option value="ligero">Ligero</option>
                    <option value="moderado">Moderado</option>
                    <option value="activo">Activo</option>
                    <option value="muy_activo">Muy Activo</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Conditions */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Condiciones</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="has_diabetes"
                    checked={formData.has_diabetes === 1}
                    onChange={handleChange}
                    className="rounded"
                  />
                  <label>Diabetes</label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="has_hypertension"
                    checked={formData.has_hypertension === 1}
                    onChange={handleChange}
                    className="rounded"
                  />
                  <label>Hipertensión</label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="has_bloating"
                    checked={formData.has_bloating === 1}
                    onChange={handleChange}
                    className="rounded"
                  />
                  <label>Distensión Abdominal</label>
                </div>
                <div>
                  <label className="label">Dieta</label>
                  <select
                    name="is_vegetarian"
                    value={formData.is_vegetarian}
                    onChange={handleChange}
                    className="input"
                  >
                    <option value={0}>Omnívoro</option>
                    <option value={1}>Vegetariano</option>
                    <option value={2}>Vegano</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Medical History */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Historia Clínica</h3>
              <div className="space-y-4">
                <div>
                  <label className="label">Historia Médica</label>
                  <textarea
                    name="medical_history"
                    value={formData.medical_history}
                    onChange={handleChange}
                    className="input"
                    rows="3"
                  />
                </div>
                <div>
                  <label className="label">Historia Nutricional</label>
                  <textarea
                    name="nutritional_history"
                    value={formData.nutritional_history}
                    onChange={handleChange}
                    className="input"
                    rows="3"
                  />
                </div>
                <div>
                  <label className="label">Alergias</label>
                  <textarea
                    name="allergies"
                    value={formData.allergies}
                    onChange={handleChange}
                    className="input"
                    rows="2"
                  />
                </div>
                <div>
                  <label className="label">Medicamentos</label>
                  <textarea
                    name="medications"
                    value={formData.medications}
                    onChange={handleChange}
                    className="input"
                    rows="2"
                  />
                </div>
                <div>
                  <label className="label">Otras Condiciones</label>
                  <textarea
                    name="other_conditions"
                    value={formData.other_conditions}
                    onChange={handleChange}
                    className="input"
                    rows="2"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Buttons */}
        <div className="flex justify-end space-x-4 pt-6 border-t">
          <button
            type="button"
            onClick={onCancel}
            className="btn-secondary"
            disabled={loading}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
          >
            {loading ? 'Guardando...' : (patient ? 'Actualizar' : 'Crear Paciente')}
          </button>
        </div>
      </form>
    </div>
  )
}

export default PatientForm


