<template>
  <div class="dish-card">
    <div class="image-wrapper">
      <img :src="dish.image || '/placeholder-dish.jpg'" :alt="dish.name" />
    </div>
    <div class="content">
      <h3>{{ dish.name }}</h3>
      <p class="description">{{ dish.description }}</p>
      <div class="footer">
        <span class="price">{{ dish.price }} ₽</span>
        <button class="add-button" @click.stop="$emit('add-to-cart', dish)">
          Добавить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  dish: {
    id: number
    name: string
    description: string
    price: number
    image?: string
  }
}>()

defineEmits(['add-to-cart'])
</script>

<style scoped>
.dish-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.dish-card:hover {
  transform: translateY(-2px);
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
  font-size: 1.1rem;
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

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-weight: bold;
}

.add-button {
  padding: 0.25rem 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-button:hover {
  background: #2563eb;
}
</style>