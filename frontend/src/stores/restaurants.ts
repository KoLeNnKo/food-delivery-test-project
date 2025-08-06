import { defineStore } from 'pinia'
import { getRestaurants } from '@/api/restaurants'

interface Restaurant {
  id: number
  name: string
  // ... другие поля
}

export const useRestaurantsStore = defineStore('restaurants', {
  state: () => ({
    restaurants: [] as Restaurant[],
    isLoading: false,
    error: null as string | null
  }),
  actions: {
    async fetchRestaurants() {
      this.isLoading = true
      try {
        const response = await getRestaurants()
        this.restaurants = response.data
      } catch (error) {
        this.error = 'Ошибка загрузки ресторанов'
      } finally {
        this.isLoading = false
      }
    }
  }
})