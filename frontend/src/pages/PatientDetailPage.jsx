import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Edit, Calculator, FileText, Calendar, Plus, Heart, Sparkles } from 'lucide-react'
import { patientsAPI, consultationsAPI, mealPlansAPI, preferencesAPI } from '../api/axios'
import PatientForm from '../components/PatientForm'
import ConsultationForm from '../components/ConsultationForm'
import PreferencesForm from '../components/PreferencesForm'

function PatientDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [patient, setPatient] = useState(null)
  const [calculations, setCalculations] = useState(null)
  const [consultations, setConsultations] = useState([])
  const [mealPlans, setMealPlans] = useState([])
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showEditForm, setShowEditForm] = useState(false)
  const [showConsultationForm, setShowConsultationForm] = useState(false)
  const [showPreferencesForm, setShowPreferencesForm] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadPatientData()
  }, [id])

  const loadPatientData = async () => {
    try {
      const [patientRes, calcRes, consultRes, mealPlanRes] = await Promise.all([
        patientsAPI.getById(id),
        patientsAPI.getCalculations(id),
        consultationsAPI.getByPatientId(id),
        mealPlansAPI.getByPatientId(id)
      ])
      
      setPatient(patientRes.data)
      setCalculations(calcRes.data)
      setConsultations(consultRes.data)
      setMealPlans(mealPlanRes.data)
    } catch (error) {
      console.error('Error loading patient data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateSuccess = () => {
    setShowEditForm(false)
    loadPatientData()
  }

  const handleConsultationSuccess = () => {
    setShowConsultationForm(false)
    loadPatientData()
  }

  const handlePreferencesSuccess = () => {
    setShowPreferencesForm(false)
    loadRecommendations()
  }

  const loadRecommendations = async () => {
    try {
      const response = await preferencesAPI.getRecommendations(id)
      setRecommendations(response.data)
    } catch (error) {
      setRecommendations(null)
    }
  }

  useEffect(() => {
    if (activeTab === 'preferences') {
      loadRecommendations()
    }
  }, [activeTab, id])

  if (loading) {
    return <div className="text-center py-8">Cargando información del paciente...</div>
  }

  if (!patient) {
    return <div className="text-center py-8">Paciente no encontrado</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/patients')}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            <ArrowLeft size={24} />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {patient.first_name} {patient.last_name}
            </h1>
            <p className="text-gray-600">{patient.identification}</p>
          </div>
        </div>
        <button
          onClick={() => setShowEditForm(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Edit size={20} />
          <span>Editar</span>
        </button>
      </div>

      {/* Edit Form Modal */}
      {showEditForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Editar Paciente</h2>
                <button
                  onClick={() => setShowEditForm(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  &times;
                </button>
              </div>
              <PatientForm
                patient={patient}
                onSuccess={handleUpdateSuccess}
                onCancel={() => setShowEditForm(false)}
              />
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex space-x-4 border-b overflow-x-auto">
        <TabButton
          active={activeTab === 'overview'}
          onClick={() => setActiveTab('overview')}
          icon={<FileText size={20} />}
          text="Información General"
        />
        <TabButton
          active={activeTab === 'calculations'}
          onClick={() => setActiveTab('calculations')}
          icon={<Calculator size={20} />}
          text="Cálculos"
        />
        <TabButton
          active={activeTab === 'consultations'}
          onClick={() => setActiveTab('consultations')}
          icon={<Calendar size={20} />}
          text="Consultas"
        />
        <TabButton
          active={activeTab === 'preferences'}
          onClick={() => setActiveTab('preferences')}
          icon={<Heart size={20} />}
          text="Preferencias"
        />
      </div>

      {/* Modals */}
      {showConsultationForm && (
        <ConsultationForm
          patientId={parseInt(id)}
          patientName={`${patient.first_name} ${patient.last_name}`}
          onSuccess={handleConsultationSuccess}
          onClose={() => setShowConsultationForm(false)}
        />
      )}

      {showPreferencesForm && (
        <PreferencesForm
          patientId={parseInt(id)}
          patientName={`${patient.first_name} ${patient.last_name}`}
          onSuccess={handlePreferencesSuccess}
          onClose={() => setShowPreferencesForm(false)}
        />
      )}

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <InfoCard title="Información Personal">
            <InfoRow label="Edad" value={`${calculateAge(patient.birth_date)} años`} />
            <InfoRow label="Género" value={patient.gender} />
            <InfoRow label="Fecha de Nacimiento" value={formatDate(patient.birth_date)} />
          </InfoCard>

          <InfoCard title="Datos Antropométricos">
            {consultations.length > 0 ? (
              <>
                <div className="mb-2 pb-2 border-b">
                  <p className="text-xs text-gray-500">
                    Última consulta: {formatDate(consultations[0].consultation_date)}
                  </p>
                </div>
                <InfoRow label="Peso" value={`${consultations[0].weight} kg`} />
                {consultations[0].weight_change && (
                  <InfoRow 
                    label="Cambio de peso" 
                    value={
                      <span className={consultations[0].weight_change > 0 ? 'text-red-600' : 'text-green-600'}>
                        {consultations[0].weight_change > 0 ? '+' : ''}{consultations[0].weight_change.toFixed(1)} kg
                      </span>
                    } 
                  />
                )}
                <InfoRow label="Altura" value={`${consultations[0].height} cm`} />
                <InfoRow label="IMC" value={consultations[0].bmi?.toFixed(2)} />
                {consultations[0].body_fat_percentage && (
                  <InfoRow label="% Grasa Corporal" value={`${consultations[0].body_fat_percentage}%`} />
                )}
                {consultations[0].muscle_mass && (
                  <InfoRow label="Masa Muscular" value={`${consultations[0].muscle_mass} kg`} />
                )}
                {consultations[0].waist_circumference && (
                  <InfoRow label="Cintura" value={`${consultations[0].waist_circumference} cm`} />
                )}
                {consultations[0].hip_circumference && (
                  <InfoRow label="Cadera" value={`${consultations[0].hip_circumference} cm`} />
                )}
              </>
            ) : (
              <>
                <InfoRow label="Peso" value={`${patient.weight} kg`} />
                <InfoRow label="Altura" value={`${patient.height} cm`} />
                <InfoRow label="IMC" value={calculations?.bmi.toFixed(2)} />
                <InfoRow label="Categoría IMC" value={calculations?.bmi_category} />
                <div className="mt-4 pt-4 border-t">
                  <p className="text-sm text-gray-500 text-center">
                    Sin consultas registradas. Los datos mostrados son del perfil base.
                  </p>
                </div>
              </>
            )}
          </InfoCard>

          <InfoCard title="Tipo de Paciente">
            <InfoRow label="Clasificación" value={patient.patient_type} />
            <InfoRow label="Nivel de Actividad" value={patient.activity_level} />
            <InfoRow label="Tipo de Dieta" value={getDietType(patient.is_vegetarian)} />
          </InfoCard>

          <InfoCard title="Condiciones">
            <div className="space-y-2">
              {patient.has_diabetes === 1 && <Badge text="Diabetes" color="bg-red-100 text-red-800" />}
              {patient.has_hypertension === 1 && <Badge text="Hipertensión" color="bg-orange-100 text-orange-800" />}
              {patient.has_bloating === 1 && <Badge text="Distensión Abdominal" color="bg-yellow-100 text-yellow-800" />}
              {patient.other_conditions && (
                <p className="text-sm text-gray-700 mt-2">{patient.other_conditions}</p>
              )}
            </div>
          </InfoCard>

          {patient.medical_history && (
            <InfoCard title="Historia Médica">
              <p className="text-gray-700 whitespace-pre-wrap">{patient.medical_history}</p>
            </InfoCard>
          )}

          {patient.nutritional_history && (
            <InfoCard title="Historia Nutricional">
              <p className="text-gray-700 whitespace-pre-wrap">{patient.nutritional_history}</p>
            </InfoCard>
          )}

          {patient.allergies && (
            <InfoCard title="Alergias">
              <p className="text-gray-700 whitespace-pre-wrap">{patient.allergies}</p>
            </InfoCard>
          )}

          {patient.medications && (
            <InfoCard title="Medicamentos">
              <p className="text-gray-700 whitespace-pre-wrap">{patient.medications}</p>
            </InfoCard>
          )}
        </div>
      )}

      {activeTab === 'calculations' && calculations && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <CalculationCard
            title="IMC"
            value={calculations.bmi.toFixed(2)}
            subtitle={calculations.bmi_category}
            color="bg-blue-500"
          />
          <CalculationCard
            title="Peso Ideal"
            value={`${calculations.ideal_weight.toFixed(1)} kg`}
            subtitle="Fórmula de Devine"
            color="bg-green-500"
          />
          <CalculationCard
            title="Peso Ajustado"
            value={`${calculations.adjusted_weight.toFixed(1)} kg`}
            subtitle="Para cálculos nutricionales"
            color="bg-purple-500"
          />
          <CalculationCard
            title="TMB"
            value={`${calculations.tmb.toFixed(0)} kcal`}
            subtitle="Tasa Metabólica Basal"
            color="bg-orange-500"
          />
          <CalculationCard
            title="Requerimiento Calórico"
            value={`${calculations.caloric_requirement.toFixed(0)} kcal/día`}
            subtitle="Total diario"
            color="bg-red-500"
          />
          <CalculationCard
            title="Proteínas"
            value={`${calculations.proteins_g.toFixed(1)} g`}
            subtitle="Por día"
            color="bg-pink-500"
          />
          <CalculationCard
            title="Carbohidratos"
            value={`${calculations.carbs_g.toFixed(1)} g`}
            subtitle="Por día"
            color="bg-yellow-500"
          />
          <CalculationCard
            title="Grasas"
            value={`${calculations.fats_g.toFixed(1)} g`}
            subtitle="Por día"
            color="bg-indigo-500"
          />
        </div>
      )}

      {activeTab === 'consultations' && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <button
              onClick={() => setShowConsultationForm(true)}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus size={20} />
              <span>Nueva Consulta</span>
            </button>
          </div>
          
          {consultations.length === 0 ? (
            <div className="card text-center py-12">
              <Calendar className="mx-auto text-gray-400 mb-4" size={64} />
              <p className="text-gray-600 text-lg mb-4">No hay consultas registradas</p>
              <button
                onClick={() => setShowConsultationForm(true)}
                className="btn-primary inline-flex items-center space-x-2"
              >
                <Plus size={20} />
                <span>Crear Primera Consulta</span>
              </button>
            </div>
          ) : (
            consultations.map((consultation) => (
              <ConsultationCard key={consultation.id} consultation={consultation} />
            ))
          )}
        </div>
      )}

      {activeTab === 'preferences' && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <button
              onClick={() => setShowPreferencesForm(true)}
              className="btn-primary flex items-center space-x-2"
            >
              <Heart size={20} />
              <span>{recommendations?.preferences_configured ? 'Editar' : 'Configurar'} Preferencias</span>
            </button>
          </div>

          {!recommendations || !recommendations.preferences_configured ? (
            <div className="card text-center py-12">
              <Heart className="mx-auto text-gray-400 mb-4" size={64} />
              <p className="text-gray-600 text-lg mb-4">No hay preferencias configuradas</p>
              <button
                onClick={() => setShowPreferencesForm(true)}
                className="btn-primary inline-flex items-center space-x-2"
              >
                <Plus size={20} />
                <span>Configurar Preferencias</span>
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Recomendaciones Personalizadas */}
              <div className="card bg-gradient-to-r from-green-50 to-blue-50">
                <div className="flex items-center mb-4">
                  <Sparkles className="text-green-600 mr-2" size={24} />
                  <h3 className="text-xl font-bold text-gray-900">Recomendaciones Personalizadas</h3>
                </div>
                <p className="text-sm text-gray-600 mb-6">
                  Basadas en las preferencias y condiciones de {recommendations.patient_name}
                </p>

                <div className="space-y-6">
                  {recommendations.recommendations.map((rec, index) => (
                    <div key={index} className="bg-white rounded-lg p-4 shadow-sm">
                      <h4 className="font-semibold text-lg mb-2 text-green-700">
                        {rec.category}
                      </h4>
                      <p className="text-gray-700 font-medium mb-3">{rec.title}</p>
                      <ul className="space-y-2">
                        {rec.items.map((item, itemIndex) => (
                          <li key={itemIndex} className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span className="text-gray-600 text-sm">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function TabButton({ active, onClick, icon, text }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors ${
        active
          ? 'border-primary-600 text-primary-600 font-medium'
          : 'border-transparent text-gray-600 hover:text-gray-900'
      }`}
    >
      {icon}
      <span>{text}</span>
    </button>
  )
}

function InfoCard({ title, children }) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      {children}
    </div>
  )
}

function InfoRow({ label, value }) {
  return (
    <div className="flex justify-between py-2 border-b last:border-0">
      <span className="text-gray-600">{label}:</span>
      <span className="font-medium">{value}</span>
    </div>
  )
}

function CalculationCard({ title, value, subtitle, color }) {
  return (
    <div className="card">
      <div className={`${color} w-12 h-12 rounded-lg flex items-center justify-center text-white mb-4`}>
        <Calculator size={24} />
      </div>
      <h3 className="text-sm text-gray-600 mb-1">{title}</h3>
      <p className="text-2xl font-bold mb-1">{value}</p>
      <p className="text-sm text-gray-500">{subtitle}</p>
    </div>
  )
}

function ConsultationCard({ consultation }) {
  return (
    <div className="card">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="font-semibold text-lg">
            Consulta - {formatDate(consultation.consultation_date)}
          </h3>
          <p className="text-sm text-gray-600">
            {new Date(consultation.consultation_date).toLocaleTimeString('es-CO')}
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">IMC</p>
          <p className="text-xl font-bold">{consultation.bmi?.toFixed(2)}</p>
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-600">Peso</p>
          <p className="font-medium">{consultation.weight} kg</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Altura</p>
          <p className="font-medium">{consultation.height} cm</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Calorías</p>
          <p className="font-medium">{consultation.caloric_requirement?.toFixed(0)} kcal</p>
        </div>
      </div>
      
      {consultation.notes && (
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-700 mb-1">Notas:</p>
          <p className="text-sm text-gray-600">{consultation.notes}</p>
        </div>
      )}
      
      {consultation.recommendations && (
        <div>
          <p className="text-sm font-medium text-gray-700 mb-1">Recomendaciones:</p>
          <p className="text-sm text-gray-600">{consultation.recommendations}</p>
        </div>
      )}
    </div>
  )
}

function Badge({ text, color }) {
  return (
    <span className={`${color} px-3 py-1 rounded-full text-sm font-medium inline-block`}>
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

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function getDietType(value) {
  if (value === 1) return 'Vegetariano'
  if (value === 2) return 'Vegano'
  return 'Omnívoro'
}

export default PatientDetailPage


