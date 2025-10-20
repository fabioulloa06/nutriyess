import { useState, useEffect } from 'react'
import { preferencesAPI } from '../api/axios'
import { X, Save, Heart, AlertCircle, Clock, DollarSign, ChefHat } from 'lucide-react'

export default function PreferencesForm({ patientId, patientName, onSuccess, onClose }) {
  const [formData, setFormData] = useState({
    patient_id: patientId,
    favorite_foods: '',
    disliked_foods: '',
    allergies: '',
    preferred_cooking_methods: '',
    cultural_restrictions: '',
    budget_level: 'medio',
    cooking_time_available: 'medio',
    likes_sweet: 3,
    likes_salty: 3,
    likes_spicy: 3,
    likes_sour: 3,
    likes_bitter: 3,
    prefers_soft_textures: true,
    prefers_crunchy_textures: true,
    breakfast_time: '',
    lunch_time: '',
    dinner_time: '',
    snacks_per_day: 2,
    additional_notes: ''
  })

  const [loading, setLoading] = useState(false)
  const [isEditing, setIsEditing] = useState(false)

  useEffect(() => {
    // Check if preferences already exist
    const loadPreferences = async () => {
      try {
        const response = await preferencesAPI.getByPatientId(patientId)
        setFormData(response.data)
        setIsEditing(true)
      } catch (error) {
        // No preferences found, keep empty form
        setIsEditing(false)
      }
    }
    loadPreferences()
  }, [patientId])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : 
              type === 'number' ? parseInt(value) : 
              value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (isEditing) {
        await preferencesAPI.update(patientId, formData)
        alert('✅ Preferencias actualizadas exitosamente')
      } else {
        await preferencesAPI.create(formData)
        alert('✅ Preferencias creadas exitosamente')
      }
      onSuccess()
    } catch (error) {
      console.error('Error saving preferences:', error)
      alert('❌ Error: ' + (error.response?.data?.detail || error.message))
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
            <h2 className="text-2xl font-bold text-gray-900">
              {isEditing ? 'Editar' : 'Configurar'} Preferencias Alimenticias
            </h2>
            <p className="text-sm text-gray-600">Paciente: {patientName}</p>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={24} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6 max-h-[calc(100vh-16rem)] overflow-y-auto">
          {/* Alimentos Favoritos y No Favoritos */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center">
              <Heart className="mr-2 text-red-500" size={20} />
              Preferencias de Alimentos
            </h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Alimentos Favoritos
              </label>
              <textarea
                name="favorite_foods"
                value={formData.favorite_foods}
                onChange={handleChange}
                rows="2"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                placeholder="Ej: Aguacate, pollo, arroz integral, frutas tropicales..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Alimentos que No Le Gustan
              </label>
              <textarea
                name="disliked_foods"
                value={formData.disliked_foods}
                onChange={handleChange}
                rows="2"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                placeholder="Ej: Brócoli, pescado, hígado..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center">
                <AlertCircle className="mr-1 text-red-500" size={16} />
                Alergias Alimentarias
              </label>
              <textarea
                name="allergies"
                value={formData.allergies}
                onChange={handleChange}
                rows="2"
                className="w-full px-3 py-2 border border-red-300 rounded-lg focus:ring-2 focus:ring-red-500"
                placeholder="Ej: Maní, mariscos, lactosa..."
              />
            </div>
          </div>

          {/* Preferencias de Cocción */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center">
              <ChefHat className="mr-2 text-orange-500" size={20} />
              Métodos de Cocción y Restricciones
            </h3>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Métodos de Cocción Preferidos
              </label>
              <textarea
                name="preferred_cooking_methods"
                value={formData.preferred_cooking_methods}
                onChange={handleChange}
                rows="2"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                placeholder="Ej: Al vapor, asado, hervido, al horno..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Restricciones Culturales/Religiosas
              </label>
              <input
                type="text"
                name="cultural_restrictions"
                value={formData.cultural_restrictions}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                placeholder="Ej: No cerdo, vegetariano, halal, kosher..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center">
                  <DollarSign className="mr-1 text-green-600" size={16} />
                  Nivel de Presupuesto
                </label>
                <select
                  name="budget_level"
                  value={formData.budget_level}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                >
                  <option value="bajo">Bajo</option>
                  <option value="medio">Medio</option>
                  <option value="alto">Alto</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center">
                  <Clock className="mr-1 text-blue-600" size={16} />
                  Tiempo Disponible para Cocinar
                </label>
                <select
                  name="cooking_time_available"
                  value={formData.cooking_time_available}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                >
                  <option value="poco">Poco (&lt; 15 min)</option>
                  <option value="medio">Medio (15-30 min)</option>
                  <option value="mucho">Mucho (&gt; 30 min)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Preferencias de Sabor */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Preferencias de Sabor</h3>
            <p className="text-sm text-gray-600">1 = No le gusta, 5 = Le encanta</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Dulce: {formData.likes_sweet}
                </label>
                <input
                  type="range"
                  name="likes_sweet"
                  min="1"
                  max="5"
                  value={formData.likes_sweet}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Salado: {formData.likes_salty}
                </label>
                <input
                  type="range"
                  name="likes_salty"
                  min="1"
                  max="5"
                  value={formData.likes_salty}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Picante: {formData.likes_spicy}
                </label>
                <input
                  type="range"
                  name="likes_spicy"
                  min="1"
                  max="5"
                  value={formData.likes_spicy}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ácido: {formData.likes_sour}
                </label>
                <input
                  type="range"
                  name="likes_sour"
                  min="1"
                  max="5"
                  value={formData.likes_sour}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Amargo: {formData.likes_bitter}
                </label>
                <input
                  type="range"
                  name="likes_bitter"
                  min="1"
                  max="5"
                  value={formData.likes_bitter}
                  onChange={handleChange}
                  className="w-full"
                />
              </div>
            </div>
          </div>

          {/* Texturas */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Texturas Preferidas</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="prefers_soft_textures"
                  checked={formData.prefers_soft_textures}
                  onChange={handleChange}
                  className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
                <span className="text-sm font-medium text-gray-700">Texturas Suaves</span>
              </label>

              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  name="prefers_crunchy_textures"
                  checked={formData.prefers_crunchy_textures}
                  onChange={handleChange}
                  className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
                <span className="text-sm font-medium text-gray-700">Texturas Crujientes</span>
              </label>
            </div>
          </div>

          {/* Horarios de Comida */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center">
              <Clock className="mr-2 text-blue-500" size={20} />
              Horarios de Comida
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Desayuno
                </label>
                <input
                  type="time"
                  name="breakfast_time"
                  value={formData.breakfast_time}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Almuerzo
                </label>
                <input
                  type="time"
                  name="lunch_time"
                  value={formData.lunch_time}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cena
                </label>
                <input
                  type="time"
                  name="dinner_time"
                  value={formData.dinner_time}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Snacks por Día
              </label>
              <select
                name="snacks_per_day"
                value={formData.snacks_per_day}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              >
                <option value="0">0 (sin snacks)</option>
                <option value="1">1 snack</option>
                <option value="2">2 snacks</option>
                <option value="3">3 snacks</option>
                <option value="4">4+ snacks</option>
              </select>
            </div>
          </div>

          {/* Notas Adicionales */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notas Adicionales
            </label>
            <textarea
              name="additional_notes"
              value={formData.additional_notes}
              onChange={handleChange}
              rows="3"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              placeholder="Cualquier información adicional relevante..."
            />
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end space-x-3 pt-6 border-t sticky bottom-0 bg-white">
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
              <span>{loading ? 'Guardando...' : isEditing ? 'Actualizar' : 'Guardar'} Preferencias</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

