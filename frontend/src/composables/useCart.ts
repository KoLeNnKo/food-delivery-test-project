import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import type { Dish } from '@/types/models'

export const useCart = () => {
  const cartStore = useCartStore()
  const isProcessing = ref(false)

  const addItem = async (dish: Dish, quantity: number = 1) => {
    try {
      isProcessing.value = true
      await cartStore.addItem(dish, quantity)
    } finally {
      isProcessing.value = false
    }
  }

  const updateItem = async (dishId: number, quantity: number) => {
    try {
      isProcessing.value = true
      await cartStore.updateItem(dishId, quantity)
    } finally {
      isProcessing.value = false
    }
  }

  const removeItem = async (dishId: number) => {
    try {
      isProcessing.value = true
      await cartStore.removeItem(dishId)
    } finally {
      isProcessing.value = false
    }
  }

  const checkout = async () => {
    try {
      isProcessing.value = true
      const order = await cartStore.checkout()
      return order
    } finally {
      isProcessing.value = false
    }
  }

  return {
    items: cartStore.items,
    total: cartStore.total,
    isEmpty: cartStore.isEmpty,
    restaurant: cartStore.restaurant,
    addItem,
    updateItem,
    removeItem,
    checkout,
    isProcessing
  }
}