<template>
  <div class="auth-page">
    <div class="auth-tabs">
      <button
        @click="switchTab('login')"
        :class="{ 'active': activeTab === 'login' }"
      >
        Вход
      </button>
      <button
        @click="switchTab('register')"
        :class="{ 'active': activeTab === 'register' }"
      >
        Регистрация
      </button>
    </div>

    <!-- Форма входа -->
    <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" novalidate>
      <div class="form-group" :class="{ 'error': v$.loginForm.email.$error }">
        <label>Email</label>
        <input
          v-model="loginForm.email"
          type="email"
          @blur="v$.loginForm.email.$touch()"
          placeholder="your@email.com"
        />
        <div v-if="v$.loginForm.email.$error" class="validation-error">
          {{ v$.loginForm.email.$errors[0].$message }}
        </div>
      </div>

      <div class="form-group" :class="{ 'error': v$.loginForm.password.$error }">
        <label>Пароль</label>
        <input
          v-model="loginForm.password"
          type="password"
          @blur="v$.loginForm.password.$touch()"
          placeholder="••••••••"
        />
        <div v-if="v$.loginForm.password.$error" class="validation-error">
          {{ v$.loginForm.password.$errors[0].$message }}
        </div>
      </div>

      <button type="submit" :disabled="v$.loginForm.$invalid || isLoading">
        <span v-if="!isLoading">Войти</span>
        <Spinner v-else size="small" />
      </button>
    </form>

    <!-- Форма регистрации -->
    <form v-else @submit.prevent="handleRegister" novalidate>
      <div class="form-group" :class="{ 'error': v$.registerForm.email.$error }">
        <label>Email</label>
        <input
          v-model="registerForm.email"
          type="email"
          @blur="v$.registerForm.email.$touch()"
          placeholder="your@email.com"
        />
        <div v-if="v$.registerForm.email.$error" class="validation-error">
          {{ v$.registerForm.email.$errors[0].$message }}
        </div>
      </div>

      <div class="form-group" :class="{ 'error': v$.registerForm.password.$error }">
        <label>Пароль</label>
        <input
          v-model="registerForm.password"
          type="password"
          @blur="v$.registerForm.password.$touch()"
          placeholder="••••••••"
        />
        <div v-if="v$.registerForm.password.$error" class="validation-error">
          <div v-for="error in v$.registerForm.password.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </div>
      </div>

      <div class="form-group" :class="{ 'error': v$.registerForm.confirmPassword.$error }">
        <label>Подтвердите пароль</label>
        <input
          v-model="registerForm.confirmPassword"
          type="password"
          @blur="v$.registerForm.confirmPassword.$touch()"
          placeholder="••••••••"
        />
        <div v-if="v$.registerForm.confirmPassword.$error" class="validation-error">
          {{ v$.registerForm.confirmPassword.$errors[0].$message }}
        </div>
      </div>

      <button type="submit" :disabled="v$.registerForm.$invalid || isLoading">
        <span v-if="!isLoading">Зарегистрироваться</span>
        <Spinner v-else size="small" />
      </button>
    </form>

    <div v-if="apiError" class="error-message">
      {{ apiError }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs, helpers } from '@vuelidate/validators'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Spinner from '@/components/ui/Spinner.vue'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref<'login' | 'register'>('login')
const isLoading = ref(false)
const apiError = ref('')

const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

// Правила валидации
const rules = computed(() => ({
  loginForm: {
    email: {
      required: helpers.withMessage('Email обязателен', required),
      email: helpers.withMessage('Введите корректный email', email)
    },
    password: {
      required: helpers.withMessage('Пароль обязателен', required),
      minLength: helpers.withMessage(
        'Пароль должен быть не менее 6 символов',
        minLength(6)
      )
    }
  },
  registerForm: {
    email: {
      required: helpers.withMessage('Email обязателен', required),
      email: helpers.withMessage('Введите корректный email', email)
    },
    password: {
      required: helpers.withMessage('Пароль обязателен', required),
      minLength: helpers.withMessage(
        'Пароль должен быть не менее 8 символов',
        minLength(8)
      ),
      containsUppercase: helpers.withMessage(
        'Должен содержать заглавную букву',
        (value: string) => /[A-Z]/.test(value)
      ),
      containsNumber: helpers.withMessage(
        'Должен содержать цифру',
        (value: string) => /[0-9]/.test(value)
      )
    },
    confirmPassword: {
      required: helpers.withMessage('Подтвердите пароль', required),
      sameAs: helpers.withMessage(
        'Пароли не совпадают',
        sameAs(registerForm.value.password)
      )
    }
  }
}))

const v$ = useVuelidate(rules, { loginForm, registerForm })

const switchTab = (tab: 'login' | 'register') => {
  activeTab.value = tab
  apiError.value = ''
  v$.value.$reset()
}

const handleLogin = async () => {
  const isValid = await v$.value.loginForm.$validate()
  if (!isValid) return

  try {
    isLoading.value = true
    await authStore.login(loginForm.value.email, loginForm.value.password)
    router.push('/')
  } catch (error) {
    apiError.value = 'Неверный email или пароль'
  } finally {
    isLoading.value = false
  }
}

const handleRegister = async () => {
  const isValid = await v$.value.registerForm.$validate()
  if (!isValid) return

  try {
    isLoading.value = true
    await authStore.register(
      registerForm.value.email,
      registerForm.value.password
    )
    switchTab('login')
  } catch (error) {
    apiError.value = 'Ошибка регистрации. Возможно, email уже занят'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.auth-tabs {
  display: flex;
  margin-bottom: 1.5rem;
}

.auth-tabs button {
  flex: 1;
  padding: 0.5rem;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
}

.auth-tabs button.active {
  background: #3b82f6;
  color: white;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  transition: border-color 0.3s;
}

.form-group.error input {
  border-color: #ef4444;
}

.validation-error {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  min-height: 1rem;
}

button[type='submit'] {
  width: 100%;
  padding: 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: opacity 0.3s;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  color: #ef4444;
  text-align: center;
  padding: 0.5rem;
  background: #fee2e2;
  border-radius: 4px;
}
</style>