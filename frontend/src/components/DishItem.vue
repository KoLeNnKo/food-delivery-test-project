<template>
  <div class="dish-item" :class="{ 'unavailable': !dish.is_available }">
    <div class="dish-info">
      <h3>{{ dish.name }}</h3>
      <p class="description">{{ dish.description }}</p>
      <div v-if="dish.ingredients" class="ingredients">
        <span>Состав: {{ dish.ingredients.join(', ') }}</span>
      </div>
      <div class="weight" v-if="dish.weight">{{ dish.weight }}</div>
    </div>

    <div class="dish-controls">
      <span class="price">{{ dish.price }} ₽</span>
      <button
        v-if="dish.is_available"
        class="add-button"
        @click="addToCart"
        :disabled="isAdding"
      >
        <span v-if="!isAdding">+ Добавить</span>
        <Spinner v-else size="small" />
      </button>
      <div v-else class="unavailable-label">Нет в наличии</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Dish } from '@/types/models'
import Spinner from '@/components/ui/Spinner.vue'
import { useCartStore } from '@/stores/cart'

const props = defineProps<{
  dish: Dish
}>()

const emit = defineEmits(['added'])

const cartStore = useCartStore()
const isAdding = ref(false)

const addToCart = async () => {
  try {
    isAdding.value = true
    await cartStore.addItem(props.dish, 1)
    emit('added')
  } finally {
    isAdding.value = false
  }
}
</script>

<style scoped>
.dish-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.dish-item.unavailable {
  opacity: 0.6;
}

.dish-info {
  flex: 1;
  padding-right: 1rem;
}

h3 {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
}

.description {
  color: #64748b;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.ingredients {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.weight {
  font-size: 0.8rem;
  color: #64748b;
}

.dish-controls {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 120px;
}

.price {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.add-button {
  padding: 0.35rem 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.add-button:hover:not(:disabled) {
  background: #2563eb;
}

.add-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.unavailable-label {
  color: #ef4444;
  font-size: 0.8rem;
  padding: 0.25rem 0;
}
</style>