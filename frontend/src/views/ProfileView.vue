<template>
  <div class="profile-view">
    <h1>Мой профиль</h1>

    <form @submit.prevent="handleSubmit" novalidate>
      <div class="form-group" :class="{ 'error': v$.email.$error }">
        <label>Email</label>
        <input
          v-model="form.email"
          type="email"
          @blur="v$.email.$touch()"
          :disabled="isLoading"
        />
        <div v-if="v$.email.$error" class="validation-error">
          {{ v$.email.$errors[0].$message }}
        </div>
      </div>

      <div class="form-group" :class="{ 'error': v$.address.$error }">
        <label>Адрес доставки</label>
        <input
          v-model="form.address"
          @blur="v$.address.$touch()"
          :disabled="isLoading"
        />
        <div v-if="v$.address.$error" class="validation-error">
          {{ v$.address.$errors[0].$message }}
        </div>
      </div>

      <div class="form-group" :class="{ 'error': v$.phone.$error }">
        <label>Телефон</label>
        <input
          v-model="form.phone"
          @blur="v$.phone.$touch()"
          :disabled="isLoading"
        />
        <div v-if="v$.phone.$error" class="validation-error">
          {{ v$.phone.$errors[0].$message }}
        </div>
      </div>

      <button type="submit" :disabled="v$.$invalid || isLoading">
        <span v-if="!isLoading">Сохранить</span>
        <Spinner v-else size="small" />
      </button>
    </form>

    <div class="section">
      <h2>Смена пароля</h2>
      <PasswordChangeForm />
    </div>

    <div v-if="apiError" class="error-message">
      {{ apiError }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'
import { useAuthStore } from '@/stores/auth'
import PasswordChangeForm from '@/components/PasswordChangeForm.vue'
import Spinner from '@/components/ui/Spinner.vue'

const authStore = useAuthStore()
const isLoading = ref(false)
const apiError = ref('')

const form = reactive({
  email: authStore.user?.email || '',
  address: authStore.user?.address || '',
  phone: authStore.user?.phone || ''
})

const rules = {
  email: { required, email },
  address: { required },
  phone: {
    required,
    valid: (value: string) => /^[\d\s+\-()]{10,}$/.test(value)
  }
}

const v$ = useVuelidate(rules, form)

const handleSubmit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  try {
    isLoading.value = true
    await authStore.updateProfile(form)
  } catch (error) {
    apiError.value = 'Ошибка при обновлении профиля'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.profile-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
}

.section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
}

h1, h2 {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
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
}

.form-group.error input {
  border-color: #ef4444;
}

.validation-error {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

button[type='submit'] {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-message {
  margin-top: 1rem;
  color: #ef4444;
  padding: 0.5rem;
  background: #fee2e2;
  border-radius: 4px;
}
</style>