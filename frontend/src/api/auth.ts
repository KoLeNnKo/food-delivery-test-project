import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})

export const login = (email: string, password: string) =>
  api.post('/auth/login', { email, password })

export const register = (email: string, password: string) =>
  api.post('/auth/register', { email, password })

// Добавляем интерцептор для JWT
api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})