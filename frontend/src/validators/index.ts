import { helpers, required, email, minLength, sameAs } from '@vuelidate/validators'

// Кастомные сообщения об ошибках
const withMessage = (validator: any, message: string) =>
  helpers.withMessage(message, validator)

export const rules = {
  required: withMessage(required, 'Обязательное поле'),
  email: withMessage(email, 'Некорректный email'),
  minLength: (length: number) =>
    withMessage(minLength(length), `Минимум ${length} символов`),
  sameAs: (field: any, name: string) =>
    withMessage(sameAs(field), `Пароли не совпадают`),
  password: {
    minLength: minLength(6),
    containsUppercase: helpers.withMessage(
      'Должен содержать заглавную букву',
      (value: string) => /[A-Z]/.test(value)
    ),
    containsNumber: helpers.withMessage(
      'Должен содержать цифру',
      (value: string) => /[0-9]/.test(value)
    )
  }
}