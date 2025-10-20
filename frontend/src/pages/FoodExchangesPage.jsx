import { useState, useEffect } from 'react'
import { Plus, ClipboardList, Filter } from 'lucide-react'
import { foodExchangesAPI } from '../api/axios'

function FoodExchangesPage() {
  const [exchanges, setExchanges] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState(null)

  const categories = [
    { value: 'cereales', label: 'Cereales', color: 'bg-amber-100 text-amber-800' },
    { value: 'leguminosas', label: 'Leguminosas', color: 'bg-brown-100 text-brown-800' },
    { value: 'verduras', label: 'Verduras', color: 'bg-green-100 text-green-800' },
    { value: 'frutas', label: 'Frutas', color: 'bg-pink-100 text-pink-800' },
    { value: 'carnes', label: 'Carnes', color: 'bg-red-100 text-red-800' },
    { value: 'lacteos', label: 'Lácteos', color: 'bg-blue-100 text-blue-800' },
    { value: 'grasas', label: 'Grasas', color: 'bg-yellow-100 text-yellow-800' },
    { value: 'azucares', label: 'Azúcares', color: 'bg-orange-100 text-orange-800' },
  ]

  useEffect(() => {
    loadExchanges()
  }, [selectedCategory])

  const loadExchanges = async () => {
    try {
      const response = await foodExchangesAPI.getAll(selectedCategory)
      setExchanges(response.data)
    } catch (error) {
      console.error('Error loading exchanges:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSeedExchanges = async () => {
    try {
      await foodExchangesAPI.seedDefault()
      loadExchanges()
      alert('Lista básica de intercambios cargada exitosamente')
    } catch (error) {
      console.error('Error seeding exchanges:', error)
      alert('Error al cargar la lista básica')
    }
  }

  const handleSeedColombianFoods = async () => {
    try {
      const response = await foodExchangesAPI.seedColombianFoods()
      loadExchanges()
      alert(`✅ ${response.data.total} alimentos colombianos cargados con micronutrientes completos`)
    } catch (error) {
      console.error('Error seeding Colombian foods:', error)
      alert('Error al cargar alimentos colombianos')
    }
  }

  if (loading) {
    return <div className="text-center py-8">Cargando intercambios...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Lista de Intercambios Alimenticios</h1>
        <div className="flex space-x-3">
          <button
            onClick={handleSeedExchanges}
            className="btn-secondary flex items-center space-x-2"
          >
            <Plus size={20} />
            <span>Lista Básica</span>
          </button>
          <button
            onClick={handleSeedColombianFoods}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus size={20} />
            <span>🇨🇴 Alimentos Colombianos</span>
          </button>
        </div>
      </div>

      {/* Description */}
      <div className="card bg-primary-50 border-l-4 border-primary-600">
        <p className="text-gray-700">
          La lista de intercambios permite crear planes de alimentación flexibles. 
          Cada alimento muestra su porción equivalente y valores nutricionales.
        </p>
      </div>

      {/* Category Filter */}
      <div className="card">
        <div className="flex items-center space-x-4 mb-4">
          <Filter size={20} className="text-gray-600" />
          <span className="font-medium">Categoría:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-2 rounded-lg transition-colors ${
              selectedCategory === null
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Todos
          </button>
          {categories.map((cat) => (
            <button
              key={cat.value}
              onClick={() => setSelectedCategory(cat.value)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                selectedCategory === cat.value
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Exchanges List */}
      {exchanges.length === 0 ? (
        <div className="card text-center py-12">
          <ClipboardList className="mx-auto text-gray-400 mb-4" size={64} />
          <p className="text-gray-600 text-lg">No hay intercambios disponibles</p>
          <p className="text-gray-500">Haz clic en "Cargar Lista Predefinida" para comenzar</p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Group by category */}
          {categories.map((category) => {
            const categoryExchanges = exchanges.filter(e => e.category === category.value)
            if (categoryExchanges.length === 0) return null

            return (
              <div key={category.value} className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <span className={`${category.color} px-3 py-1 rounded-full text-sm font-medium`}>
                    {category.label}
                  </span>
                  <span className="text-gray-600">({categoryExchanges.length} alimentos)</span>
                </div>
                
                <div className="overflow-x-auto">
                    <table className="w-full min-w-max">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-sm font-medium text-gray-700 sticky left-0 bg-gray-50">Alimento</th>
                          <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Porción</th>
                          <th className="px-4 py-3 text-center text-sm font-medium text-gray-700 bg-blue-50" colSpan="4">MACRONUTRIENTES</th>
                          <th className="px-4 py-3 text-center text-sm font-medium text-gray-700 bg-green-50" colSpan="6">MICRONUTRIENTES</th>
                          <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Notas</th>
                        </tr>
                        <tr>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 sticky left-0 bg-gray-50"></th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600"></th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-blue-50">Cal</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-blue-50">Prot</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-blue-50">Carb</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-blue-50">Grasas</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-green-50">Calcio</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-green-50">Hierro</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-green-50">Sodio</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-green-50">Potasio</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-green-50">Vit A</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600 bg-green-50">Vit C</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-600"></th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {categoryExchanges.map((exchange) => (
                          <tr key={exchange.id} className="hover:bg-gray-50">
                            <td className="px-4 py-3 text-sm font-medium text-gray-900 sticky left-0 bg-white">{exchange.name}</td>
                            <td className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">{exchange.portion_size}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{exchange.calories}</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{exchange.proteins}g</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{exchange.carbohydrates}g</td>
                            <td className="px-4 py-3 text-sm text-gray-700">{exchange.fats}g</td>
                            <td className="px-4 py-3 text-sm text-gray-600">{exchange.calcium ? `${exchange.calcium}mg` : '-'}</td>
                            <td className="px-4 py-3 text-sm text-gray-600">{exchange.iron ? `${exchange.iron}mg` : '-'}</td>
                            <td className="px-4 py-3 text-sm text-gray-600">{exchange.sodium ? `${exchange.sodium}mg` : '-'}</td>
                            <td className="px-4 py-3 text-sm text-gray-600">{exchange.potassium ? `${exchange.potassium}mg` : '-'}</td>
                            <td className="px-4 py-3 text-sm text-gray-600">{exchange.vitamin_a ? `${exchange.vitamin_a}µg` : '-'}</td>
                            <td className="px-4 py-3 text-sm text-gray-600">{exchange.vitamin_c ? `${exchange.vitamin_c}mg` : '-'}</td>
                            <td className="px-4 py-3 text-xs text-gray-500 max-w-xs truncate">{exchange.notes || '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default FoodExchangesPage


