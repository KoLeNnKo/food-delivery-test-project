<template>
  <div class="restaurant-card">
    <div class="image-wrapper">
      <img
        :src="restaurant.image || '/placeholder-restaurant.jpg'"
        :alt="restaurant.name"
      />
    </div>
    <div class="content">
      <h3>{{ restaurant.name }}</h3>
      <p class="description">{{ restaurant.description }}</p>
      <div class="meta">
        <span class="rating">★ {{ restaurant.rating }}</span>
        <span class="delivery-time">{{ restaurant.delivery_time }} мин</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  restaurant: {
    id: number
    name: string
    description: string
    rating: number
    delivery_time: string
    image: string
  }
}>()
</script>

<style scoped>
.restaurant-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.restaurant-card:hover {
  transform: translateY(-4px);
}

.image-wrapper {
  height: 160px;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.content {
  padding: 1rem;
}

h3 {
  margin: 0 0 0.5rem;
  font-size: 1.2rem;
}

.description {
  color: #64748b;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rating {
  color: #f59e0b;
  font-weight: bold;
}

.delivery-time {
  color: #64748b;
  font-size: 0.9rem;
}
</style>