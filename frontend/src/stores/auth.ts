import { defineStore } from 'pinia'
import { login as apiLogin, register as apiRegister } from '@/api/auth'
import router from '@/router'

async login(email: string, password: string) {
  try {
    const response = await apiLogin(email, password)
    if (response.data.error) {
      throw new Error(response.data.error)
    }
    this.token = response.data.access_token
    await this.fetchUser()
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Ошибка авторизации')
  }
}

interface User {
  id: number
  email: string
  role: string
}

interface AuthState {
  user: User | null
  token: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null
  }),
  actions: {
    async login(email: string, password: string) {
      try {
        const response = await apiLogin(email, password)
        this.token = response.data.access_token
        await this.fetchUser()
        router.push('/')
      } catch (error) {
        throw new Error('Неверные учетные данные')
      }
    },
    async register(email: string, password: string) {
      await apiRegister(email, password)
    },
    async fetchUser() {
      // Запрос данных пользователя по токену
    },
    logout() {
      this.user = null
      this.token = null
      router.push('/auth')
    }
  },
  persist: true // Для сохранения состояния при перезагрузке
})