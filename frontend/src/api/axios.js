import axios from 'axios';

const api = axios.create({
  baseURL: 'https://nutriyessapp.up.railway.app/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Patients API
export const patientsAPI = {
  getAll: () => api.get('/patients'),
  getById: (id) => api.get(`/patients/${id}`),
  create: (data) => api.post('/patients', data),
  update: (id, data) => api.put(`/patients/${id}`, data),
  delete: (id) => api.delete(`/patients/${id}`),
  getCalculations: (id) => api.get(`/patients/${id}/calculations`),
  search: (query) => api.get(`/patients/search/${query}`),
};

// Menus API
export const menusAPI = {
  getAll: (category) => api.get('/menus', { params: { category } }),
  getById: (id) => api.get(`/menus/${id}`),
  create: (data) => api.post('/menus', data),
  update: (id, data) => api.put(`/menus/${id}`, data),
  delete: (id) => api.delete(`/menus/${id}`),
  seedDefault: () => api.post('/menus/seed-default-menus'),
};

// Meal Plans API
export const mealPlansAPI = {
  getByPatientId: (patientId) => api.get(`/meal-plans/patient/${patientId}`),
  getById: (id) => api.get(`/meal-plans/${id}`),
  create: (data) => api.post('/meal-plans', data),
  update: (id, data) => api.put(`/meal-plans/${id}`, data),
  delete: (id) => api.delete(`/meal-plans/${id}`),
};

// Consultations API
export const consultationsAPI = {
  getByPatientId: (patientId) => api.get(`/consultations/patient/${patientId}`),
  getById: (id) => api.get(`/consultations/${id}`),
  create: (data) => api.post('/consultations', data),
  update: (id, data) => api.put(`/consultations/${id}`, data),
  delete: (id) => api.delete(`/consultations/${id}`),
  getUpcoming: () => api.get('/consultations/upcoming/all'),
};

// Food Exchanges API
export const foodExchangesAPI = {
  getAll: (category) => api.get('/food-exchanges', { params: { category } }),
  getById: (id) => api.get(`/food-exchanges/${id}`),
  create: (data) => api.post('/food-exchanges', data),
  update: (id, data) => api.put(`/food-exchanges/${id}`, data),
  delete: (id) => api.delete(`/food-exchanges/${id}`),
  seedDefault: () => api.post('/food-exchanges/seed-default-exchanges'),
  seedColombianFoods: () => api.post('/food-exchanges/seed-colombian-foods'),
};

// Snacks API
export const snacksAPI = {
  getAll: (filters) => api.get('/snacks', { params: filters }),
  getById: (id) => api.get(`/snacks/${id}`),
  create: (data) => api.post('/snacks', data),
  update: (id, data) => api.put(`/snacks/${id}`, data),
  delete: (id) => api.delete(`/snacks/${id}`),
  seedDefault: () => api.post('/snacks/seed-default-snacks'),
};

// Preferences API
export const preferencesAPI = {
  getByPatientId: (patientId) => api.get(`/preferences/patient/${patientId}`),
  create: (data) => api.post('/preferences', data),
  update: (patientId, data) => api.put(`/preferences/patient/${patientId}`, data),
  delete: (patientId) => api.delete(`/preferences/patient/${patientId}`),
  getRecommendations: (patientId) => api.get(`/preferences/patient/${patientId}/recommendations`),
};

export default api;


