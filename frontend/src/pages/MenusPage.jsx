import { useState, useEffect } from 'react'
import { Plus, BookOpen, Filter } from 'lucide-react'
import { menusAPI } from '../api/axios'

function MenusPage() {
  const [menus, setMenus] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [selectedMenu, setSelectedMenu] = useState(null)

  const categories = [
    { value: 'sano', label: 'Saludable', color: 'bg-green-100 text-green-800' },
    { value: 'diabetes', label: 'Diabetes', color: 'bg-red-100 text-red-800' },
    { value: 'hipertension', label: 'Hipertensión', color: 'bg-orange-100 text-orange-800' },
    { value: 'distension_abdominal', label: 'Distensión Abdominal', color: 'bg-yellow-100 text-yellow-800' },
    { value: 'vegetariano', label: 'Vegetariano', color: 'bg-green-100 text-green-800' },
    { value: 'vegano', label: 'Vegano', color: 'bg-emerald-100 text-emerald-800' },
    { value: 'deportista', label: 'Deportista', color: 'bg-blue-100 text-blue-800' },
  ]

  useEffect(() => {
    loadMenus()
  }, [selectedCategory])

  const loadMenus = async () => {
    try {
      const response = await menusAPI.getAll(selectedCategory)
      setMenus(response.data)
    } catch (error) {
      console.error('Error loading menus:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSeedMenus = async () => {
    try {
      await menusAPI.seedDefault()
      loadMenus()
    } catch (error) {
      console.error('Error seeding menus:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Cargando menús...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Menús Nutricionales</h1>
        <button
          onClick={handleSeedMenus}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus size={20} />
          <span>Cargar Menús Predefinidos</span>
        </button>
      </div>

      {/* Category Filter */}
      <div className="card">
        <div className="flex items-center space-x-4 mb-4">
          <Filter size={20} className="text-gray-600" />
          <span className="font-medium">Filtrar por categoría:</span>
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

      {/* Menus Grid */}
      {menus.length === 0 ? (
        <div className="card text-center py-12">
          <BookOpen className="mx-auto text-gray-400 mb-4" size={64} />
          <p className="text-gray-600 text-lg">No hay menús disponibles</p>
          <p className="text-gray-500">Haz clic en "Cargar Menús Predefinidos" para comenzar</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {menus.map((menu) => (
            <div
              key={menu.id}
              onClick={() => setSelectedMenu(menu)}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg">{menu.name}</h3>
                <span className={`${getCategoryColor(menu.category)} px-2 py-1 rounded text-xs font-medium`}>
                  {getCategoryLabel(menu.category)}
                </span>
              </div>
              
              {menu.description && (
                <p className="text-gray-600 text-sm mb-4">{menu.description}</p>
              )}
              
              {menu.calories && (
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Calorías</p>
                    <p className="font-medium">{menu.calories} kcal</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Proteínas</p>
                    <p className="font-medium">{menu.proteins} g</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Carbohidratos</p>
                    <p className="font-medium">{menu.carbohydrates} g</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Grasas</p>
                    <p className="font-medium">{menu.fats} g</p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Menu Detail Modal */}
      {selectedMenu && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h2 className="text-2xl font-bold">{selectedMenu.name}</h2>
                  <span className={`${getCategoryColor(selectedMenu.category)} px-3 py-1 rounded-full text-sm font-medium inline-block mt-2`}>
                    {getCategoryLabel(selectedMenu.category)}
                  </span>
                </div>
                <button
                  onClick={() => setSelectedMenu(null)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  &times;
                </button>
              </div>

              {selectedMenu.description && (
                <p className="text-gray-700 mb-6">{selectedMenu.description}</p>
              )}

              {/* Nutritional Info */}
              {selectedMenu.calories && (
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Calorías</p>
                    <p className="text-xl font-bold text-primary-600">{selectedMenu.calories}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Proteínas</p>
                    <p className="text-xl font-bold text-blue-600">{selectedMenu.proteins}g</p>
                  </div>
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Carbohidratos</p>
                    <p className="text-xl font-bold text-orange-600">{selectedMenu.carbohydrates}g</p>
                  </div>
                  <div className="text-center">
                    <p className="text-gray-600 text-sm">Grasas</p>
                    <p className="text-xl font-bold text-red-600">{selectedMenu.fats}g</p>
                  </div>
                  {selectedMenu.fiber && (
                    <div className="text-center">
                      <p className="text-gray-600 text-sm">Fibra</p>
                      <p className="text-xl font-bold text-green-600">{selectedMenu.fiber}g</p>
                    </div>
                  )}
                </div>
              )}

              {/* Meal Times */}
              <div className="space-y-4">
                {selectedMenu.breakfast && (
                  <MealSection title="Desayuno" content={selectedMenu.breakfast} />
                )}
                {selectedMenu.morning_snack && (
                  <MealSection title="Media Mañana" content={selectedMenu.morning_snack} />
                )}
                {selectedMenu.lunch && (
                  <MealSection title="Almuerzo" content={selectedMenu.lunch} />
                )}
                {selectedMenu.afternoon_snack && (
                  <MealSection title="Media Tarde" content={selectedMenu.afternoon_snack} />
                )}
                {selectedMenu.dinner && (
                  <MealSection title="Cena" content={selectedMenu.dinner} />
                )}
                {selectedMenu.supplements && (
                  <MealSection title="Suplementos" content={selectedMenu.supplements} />
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function MealSection({ title, content }) {
  return (
    <div className="border-l-4 border-primary-600 pl-4">
      <h4 className="font-semibold text-lg mb-2">{title}</h4>
      <p className="text-gray-700 whitespace-pre-wrap">{content}</p>
    </div>
  )
}

function getCategoryColor(category) {
  const colors = {
    'sano': 'bg-green-100 text-green-800',
    'diabetes': 'bg-red-100 text-red-800',
    'hipertension': 'bg-orange-100 text-orange-800',
    'distension_abdominal': 'bg-yellow-100 text-yellow-800',
    'vegetariano': 'bg-green-100 text-green-800',
    'vegano': 'bg-emerald-100 text-emerald-800',
    'deportista': 'bg-blue-100 text-blue-800',
  }
  return colors[category] || 'bg-gray-100 text-gray-800'
}

function getCategoryLabel(category) {
  const labels = {
    'sano': 'Saludable',
    'diabetes': 'Diabetes',
    'hipertension': 'Hipertensión',
    'distension_abdominal': 'Distensión Abdominal',
    'vegetariano': 'Vegetariano',
    'vegano': 'Vegano',
    'deportista': 'Deportista',
  }
  return labels[category] || category
}

export default MenusPage


