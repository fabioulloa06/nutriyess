import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Search, User } from 'lucide-react'
import { patientsAPI } from '../api/axios'
import PatientForm from '../components/PatientForm'

function PatientsPage() {
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    loadPatients()
  }, [])

  const loadPatients = async () => {
    try {
      const response = await patientsAPI.getAll()
      setPatients(response.data)
    } catch (error) {
      console.error('Error loading patients:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    const query = e.target.value
    setSearchQuery(query)
    
    if (query.length > 2) {
      try {
        const response = await patientsAPI.search(query)
        setPatients(response.data)
      } catch (error) {
        console.error('Error searching patients:', error)
      }
    } else if (query.length === 0) {
      loadPatients()
    }
  }

  const handlePatientCreated = () => {
    setShowForm(false)
    loadPatients()
  }

  if (loading) {
    return <div className="text-center py-8">Cargando pacientes...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Pacientes</h1>
        <button
          onClick={() => setShowForm(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus size={20} />
          <span>Nuevo Paciente</span>
        </button>
      </div>

      {/* Search */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Buscar por nombre o identificación..."
            value={searchQuery}
            onChange={handleSearch}
            className="input pl-10"
          />
        </div>
      </div>

      {/* Patient Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Nuevo Paciente</h2>
                <button
                  onClick={() => setShowForm(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  &times;
                </button>
              </div>
              <PatientForm onSuccess={handlePatientCreated} onCancel={() => setShowForm(false)} />
            </div>
          </div>
        </div>
      )}

      {/* Patients List */}
      {patients.length === 0 ? (
        <div className="card text-center py-12">
          <User className="mx-auto text-gray-400 mb-4" size={64} />
          <p className="text-gray-600 text-lg">No hay pacientes registrados</p>
          <p className="text-gray-500">Comienza agregando tu primer paciente</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {patients.map((patient) => (
            <Link
              key={patient.id}
              to={`/patients/${patient.id}`}
              className="card hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <User className="text-primary-600" size={24} />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">
                    {patient.first_name} {patient.last_name}
                  </h3>
                  <p className="text-sm text-gray-600">{patient.identification}</p>
                </div>
              </div>
              
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Edad:</span>
                  <span className="font-medium">{calculateAge(patient.birth_date)} años</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Peso:</span>
                  <span className="font-medium">{patient.weight} kg</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Altura:</span>
                  <span className="font-medium">{patient.height} cm</span>
                </div>
                <div className="flex flex-wrap gap-1 mt-3">
                  {patient.has_diabetes === 1 && <Badge text="Diabetes" color="bg-red-100 text-red-800" />}
                  {patient.has_hypertension === 1 && <Badge text="Hipertensión" color="bg-orange-100 text-orange-800" />}
                  {patient.is_vegetarian === 1 && <Badge text="Vegetariano" color="bg-green-100 text-green-800" />}
                  {patient.is_vegetarian === 2 && <Badge text="Vegano" color="bg-green-100 text-green-800" />}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

function Badge({ text, color }) {
  return (
    <span className={`${color} px-2 py-1 rounded text-xs font-medium`}>
      {text}
    </span>
  )
}

function calculateAge(birthDate) {
  const today = new Date()
  const birth = new Date(birthDate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  return age
}

export default PatientsPage


