import { useState, useEffect } from 'react'
import { Plus, Coffee } from 'lucide-react'
import { snacksAPI } from '../api/axios'

function SnacksPage() {
  const [snacks, setSnacks] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedSnack, setSelectedSnack] = useState(null)
  const [filters, setFilters] = useState({
    vegetarian: null,
    vegan: null,
    diabetic_friendly: null,
    low_sodium: null,
  })

  useEffect(() => {
    loadSnacks()
  }, [filters])

  const loadSnacks = async () => {
    try {
      const response = await snacksAPI.getAll(filters)
      setSnacks(response.data)
    } catch (error) {
      console.error('Error loading snacks:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSeedSnacks = async () => {
    try {
      await snacksAPI.seedDefault()
      loadSnacks()
    } catch (error) {
      console.error('Error seeding snacks:', error)
    }
  }

  const toggleFilter = (filterName) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: prev[filterName] === null ? true : (prev[filterName] === true ? false : null)
    }))
  }

  if (loading) {
    return <div className="text-center py-8">Cargando snacks...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Snacks Saludables</h1>
        <button
          onClick={handleSeedSnacks}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus size={20} />
          <span>Cargar Snacks Predefinidos</span>
        </button>
      </div>

      {/* Description */}
      <div className="card bg-primary-50 border-l-4 border-primary-600">
        <p className="text-gray-700">
          Demuestra a tus pacientes que comer sano puede ser delicioso y divertido. 
          Cada snack incluye receta completa e información nutricional.
        </p>
      </div>

      {/* Filters */}
      <div className="card">
        <h3 className="font-medium mb-4">Filtros:</h3>
        <div className="flex flex-wrap gap-2">
          <FilterButton
            label="Vegetariano"
            active={filters.vegetarian}
            onClick={() => toggleFilter('vegetarian')}
          />
          <FilterButton
            label="Vegano"
            active={filters.vegan}
            onClick={() => toggleFilter('vegan')}
          />
          <FilterButton
            label="Apto para Diabéticos"
            active={filters.diabetic_friendly}
            onClick={() => toggleFilter('diabetic_friendly')}
          />
          <FilterButton
            label="Bajo en Sodio"
            active={filters.low_sodium}
            onClick={() => toggleFilter('low_sodium')}
          />
        </div>
      </div>

      {/* Snacks Grid */}
      {snacks.length === 0 ? (
        <div className="card text-center py-12">
          <Coffee className="mx-auto text-gray-400 mb-4" size={64} />
          <p className="text-gray-600 text-lg">No hay snacks disponibles</p>
          <p className="text-gray-500">Haz clic en "Cargar Snacks Predefinidos" para comenzar</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {snacks.map((snack) => (
            <div
              key={snack.id}
              onClick={() => setSelectedSnack(snack)}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
            >
              <h3 className="font-semibold text-lg mb-2">{snack.name}</h3>
              
              {snack.description && (
                <p className="text-gray-600 text-sm mb-4">{snack.description}</p>
              )}
              
              {snack.calories && (
                <div className="grid grid-cols-2 gap-2 text-sm mb-4">
                  <div>
                    <p className="text-gray-600">Calorías</p>
                    <p className="font-medium">{snack.calories} kcal</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Proteínas</p>
                    <p className="font-medium">{snack.proteins}g</p>
                  </div>
                </div>
              )}
              
              <div className="flex flex-wrap gap-1">
                {snack.is_vegetarian && <Badge text="Vegetariano" color="bg-green-100 text-green-800" />}
                {snack.is_vegan && <Badge text="Vegano" color="bg-emerald-100 text-emerald-800" />}
                {snack.is_diabetic_friendly && <Badge text="Diabético" color="bg-blue-100 text-blue-800" />}
                {snack.is_low_sodium && <Badge text="Bajo en Sodio" color="bg-purple-100 text-purple-800" />}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Snack Detail Modal */}
      {selectedSnack && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold mb-2">{selectedSnack.name}</h2>
                  <div className="flex flex-wrap gap-2">
                    {selectedSnack.is_vegetarian && <Badge text="Vegetariano" color="bg-green-100 text-green-800" />}
                    {selectedSnack.is_vegan && <Badge text="Vegano" color="bg-emerald-100 text-emerald-800" />}
                    {selectedSnack.is_diabetic_friendly && <Badge text="Apto para Diabéticos" color="bg-blue-100 text-blue-800" />}
                    {selectedSnack.is_low_sodium && <Badge text="Bajo en Sodio" color="bg-purple-100 text-purple-800" />}
                  </div>
                </div>
                <button
                  onClick={() => setSelectedSnack(null)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  &times;
                </button>
              </div>

              {selectedSnack.description && (
                <p className="text-gray-700 mb-6">{selectedSnack.description}</p>
              )}

              {/* Nutritional Info */}
              {selectedSnack.calories && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Calorías</p>
                    <p className="text-xl font-bold text-primary-600">{selectedSnack.calories}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Proteínas</p>
                    <p className="text-xl font-bold text-blue-600">{selectedSnack.proteins}g</p>
                  </div>
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Carbohidratos</p>
                    <p className="text-xl font-bold text-orange-600">{selectedSnack.carbohydrates}g</p>
                  </div>
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Grasas</p>
                    <p className="text-xl font-bold text-red-600">{selectedSnack.fats}g</p>
                  </div>
                </div>
              )}

              {/* Recipe */}
              {selectedSnack.recipe && (
                <div className="border-l-4 border-primary-600 pl-4">
                  <h4 className="font-semibold text-lg mb-3">Receta:</h4>
                  <p className="text-gray-700 whitespace-pre-wrap">{selectedSnack.recipe}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function FilterButton({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-lg transition-colors ${
        active === true
          ? 'bg-primary-600 text-white'
          : active === false
          ? 'bg-red-100 text-red-700'
          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      }`}
    >
      {label}
      {active === false && ' (Excluir)'}
    </button>
  )
}

function Badge({ text, color }) {
  return (
    <span className={`${color} px-2 py-1 rounded text-xs font-medium`}>
      {text}
    </span>
  )
}

export default SnacksPage


