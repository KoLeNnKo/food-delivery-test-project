import { helpers } from '@vuelidate/validators'

export const passwordValidators = {
  minLength: helpers.withMessage('Минимум 8 символов', (val: string) => val.length >= 8),
  hasUpper: helpers.withMessage('Должна быть заглавная буква', (val: string) => /[A-Z]/.test(val)),
  hasNumber: helpers.withMessage('Должна быть цифра', (val: string) => /[0-9]/.test(val)),
  hasSpecial: helpers.withMessage(
    'Должен быть спецсимвол (!@#$%^&*)',
    (val: string) => /[!@#$%^&*]/.test(val)
  )
}

export const emailValidators = {
  required: helpers.withMessage('Обязательное поле', (val: string) => !!val),
  valid: helpers.withMessage('Некорректный email', (val: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val))
}