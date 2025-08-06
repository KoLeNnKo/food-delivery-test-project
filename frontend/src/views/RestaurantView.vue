<template>
  <div class="restaurant-view">
    <div v-if="loading" class="loading">
      <Spinner size="large" />
    </div>

    <template v-else-if="restaurant">
      <div class="restaurant-header">
        <h1>{{ restaurant.name }}</h1>
        <div class="meta">
          <span class="rating">★ {{ restaurant.rating }}</span>
          <span class="delivery-time">{{ restaurant.delivery_time }} мин</span>
        </div>
        <p class="description">{{ restaurant.description }}</p>
      </div>

      <div class="menu-section">
        <h2>Меню</h2>
        <div class="menu-grid">
          <DishCard
            v-for="dish in restaurant.menu"
            :key="dish.id"
            :dish="dish"
            @add-to-cart="addToCart"
          />
        </div>
      </div>
    </template>

    <div v-else class="not-found">
      <p>Ресторан не найден</p>
      <RouterLink to="/" class="back-button">Вернуться к списку</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getRestaurantById } from '@/api/restaurants'
import { useCartStore } from '@/stores/cart'
import DishCard from '@/components/DishCard.vue'
import Spinner from '@/components/ui/Spinner.vue'

const route = useRoute()
const cartStore = useCartStore()
const restaurant = ref(null)
const loading = ref(true)

const addToCart = (dish: any) => {
  cartStore.addItem(dish, 1)
}

onMounted(async () => {
  try {
    const response = await getRestaurantById(Number(route.params.id))
    restaurant.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки ресторана:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.restaurant-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.restaurant-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.meta {
  display: flex;
  gap: 1rem;
  margin: 0.5rem 0;
  color: #64748b;
}

.rating {
  color: #f59e0b;
  font-weight: bold;
}

.description {
  color: #475569;
}

.menu-section {
  margin-top: 2rem;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.not-found {
  text-align: center;
  padding: 2rem;
}

.back-button {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border-radius: 4px;
  text-decoration: none;
}
</style>