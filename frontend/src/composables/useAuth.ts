import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { LoginForm, RegisterForm } from '@/types/models'

export const useAuth = () => {
  const router = useRouter()
  const authStore = useAuthStore()
  const isLoading = ref(false)
  const error = ref('')

  const login = async (form: LoginForm) => {
    try {
      isLoading.value = true
      error.value = ''
      await authStore.login(form.email, form.password)
      await router.push('/')
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка авторизации'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (form: RegisterForm) => {
    try {
      isLoading.value = true
      error.value = ''
      await authStore.register(form.email, form.password)
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ошибка регистрации'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await authStore.logout()
      await router.push('/auth')
    } catch (err) {
      error.value = 'Ошибка при выходе'
    }
  }

  return {
    isLoading,
    error,
    login,
    register,
    logout,
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated
  }
}