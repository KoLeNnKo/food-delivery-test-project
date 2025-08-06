<template>
  <form @submit.prevent="handleSubmit" novalidate>
    <div class="form-group" :class="{ 'error': v$.currentPassword.$error }">
      <label>Текущий пароль</label>
      <input
        v-model="form.currentPassword"
        type="password"
        @blur="v$.currentPassword.$touch()"
      />
      <div v-if="v$.currentPassword.$error" class="validation-error">
        {{ v$.currentPassword.$errors[0].$message }}
      </div>
    </div>

    <div class="form-group" :class="{ 'error': v$.newPassword.$error }">
      <label>Новый пароль</label>
      <input
        v-model="form.newPassword"
        type="password"
        @blur="v$.newPassword.$touch()"
      />
      <div v-if="v$.newPassword.$error" class="validation-error">
        <div v-for="error in v$.newPassword.$errors" :key="error.$uid">
          {{ error.$message }}
        </div>
      </div>
    </div>

    <div class="form-group" :class="{ 'error': v$.confirmPassword.$error }">
      <label>Подтвердите пароль</label>
      <input
        v-model="form.confirmPassword"
        type="password"
        @blur="v$.confirmPassword.$touch()"
      />
      <div v-if="v$.confirmPassword.$error" class="validation-error">
        {{ v$.confirmPassword.$errors[0].$message }}
      </div>
    </div>

    <button type="submit" :disabled="v$.$invalid || isLoading">
      <span v-if="!isLoading">Сменить пароль</span>
      <Spinner v-else size="small" />
    </button>

    <div v-if="apiError" class="error-message">
      {{ apiError }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, sameAs } from '@vuelidate/validators'
import { passwordValidators } from '@/utils/validators'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isLoading = ref(false)
const apiError = ref('')

const form = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const rules = {
  currentPassword: { required },
  newPassword: {
    required,
    ...passwordValidators
  },
  confirmPassword: {
    required,
    sameAs: sameAs(form.newPassword)
  }
}

const v$ = useVuelidate(rules, form)

const handleSubmit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return

  try {
    isLoading.value = true
    await authStore.changePassword(
      form.currentPassword,
      form.newPassword
    )
    form.currentPassword = ''
    form.newPassword = ''
    form.confirmPassword = ''
    apiError.value = ''
  } catch (error) {
    apiError.value = 'Ошибка при смене пароля. Проверьте текущий пароль.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.validation-error {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

button[type='submit'] {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #10b981;
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