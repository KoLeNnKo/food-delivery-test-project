import { defineStore } from 'pinia'
import { createOrder } from '@/api/orders'
import { useAuthStore } from './auth'

interface CartItem {
  dish: {
    id: number
    name: string
    description: string
    price: number
  }
  quantity: number
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),

  getters: {
    isEmpty: (state) => state.items.length === 0,
    total: (state) => state.items.reduce(
      (sum, item) => sum + (item.dish.price * item.quantity), 0
    ),
  },

  actions: {
    addItem(dish: CartItem['dish'], quantity: number = 1) {
      const existing = this.items.find(item => item.dish.id === dish.id)

      if (existing) {
        existing.quantity += quantity
      } else {
        this.items.push({ dish, quantity })
      }
    },

    updateItem(dishId: number, quantity: number) {
      const item = this.items.find(item => item.dish.id === dishId)
      if (item) {
        item.quantity = quantity
      }
    },

    removeItem(dishId: number) {
      this.items = this.items.filter(item => item.dish.id !== dishId)
    },

    clear() {
      this.items = []
    },

    async checkout() {
      const authStore = useAuthStore()

      if (!authStore.user) {
        throw new Error('Требуется авторизация')
      }

      const orderItems = this.items.map(item => ({
        dish_id: item.dish.id,
        quantity: item.quantity
      }))

      await createOrder({
        user_id: authStore.user.id,
        items: orderItems
      })

      this.clear()
    }
  },

  persist: true // Сохраняем корзину в localStorage
})