<template>
  <div class="home-view">
    <h1>Рестораны</h1>

    <!-- Фильтры -->
    <div class="filters">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск по названию..."
      />
      <select v-model="selectedCategory">
        <option value="">Все категории</option>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
    </div>

    <!-- Список ресторанов -->
    <div v-if="isLoading" class="loading">
      <Spinner />
    </div>

    <div v-else-if="filteredRestaurants.length" class="restaurant-grid">
      <RestaurantCard
        v-for="restaurant in filteredRestaurants"
        :key="restaurant.id"
        :restaurant="restaurant"
        @click="goToRestaurant(restaurant.id)"
      />
    </div>

    <div v-else class="empty">
      <p>Рестораны не найдены</p>
      <button @click="fetchRestaurants">Попробовать снова</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRestaurants, getCategories } from '@/api/restaurants'
import RestaurantCard from '@/components/RestaurantCard.vue'
import Spinner from '@/components/ui/Spinner.vue'

const router = useRouter()
const restaurants = ref<Restaurant[]>([])
const categories = ref<Category[]>([])
const isLoading = ref(false)
const error = ref('')
const searchQuery = ref('')
const selectedCategory = ref('')

interface Restaurant {
  id: number
  name: string
  description: string
  rating: number
  delivery_time: string
  image: string
  categories: number[]
}

interface Category {
  id: number
  name: string
}

// Получение данных
const fetchRestaurants = async () => {
  try {
    isLoading.value = true
    const response = await getRestaurants()
    restaurants.value = response.data
  } catch (err) {
    error.value = 'Ошибка загрузки ресторанов'
  } finally {
    isLoading.value = false
  }
}

const fetchCategories = async () => {
  const response = await getCategories()
  categories.value = response.data
}

// Фильтрация
const filteredRestaurants = computed(() => {
  return restaurants.value.filter(restaurant => {
    const matchesSearch = restaurant.name
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase())

    const matchesCategory = selectedCategory.value
      ? restaurant.categories.includes(Number(selectedCategory.value))
      : true

    return matchesSearch && matchesCategory
  })
})

// Навигация
const goToRestaurant = (id: number) => {
  router.push(`/restaurants/${id}`)
}

// Инициализация
onMounted(() => {
  fetchRestaurants()
  fetchCategories()
})
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filters input, .filters select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.filters input {
  flex: 2;
}

.filters select {
  flex: 1;
}

.restaurant-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.empty {
  text-align: center;
  padding: 2rem;
}

.empty button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>