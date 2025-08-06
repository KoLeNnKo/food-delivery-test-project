<template>
  <form>
    <div class="form-group" :class="{ 'error': v$.address.$error }">
      <label>Адрес доставки</label>
      <input v-model="form.address" @blur="v$.address.$touch()">
      <div v-if="v$.address.$error" class="error-message">
        {{ v$.address.$errors[0].$message }}
      </div>
    </div>

    <!-- Другие поля -->
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required } from '@vuelidate/validators'

const form = reactive({
  address: '',
  phone: '',
  comment: ''
})

const rules = {
  address: { required: rules.required },
  phone: {
    required: rules.required,
    phone: helpers.withMessage(
      'Некорректный телефон',
      (val: string) => /^[\d\s+\-()]{10,}$/.test(val)
    )
  }
}

const v$ = useVuelidate(rules, form)
</script>