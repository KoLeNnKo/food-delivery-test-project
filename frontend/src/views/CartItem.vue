<template>
  <div class="cart-item">
    <div class="item-info">
      <h3>{{ item.dish.name }}</h3>
      <p>{{ item.dish.description }}</p>
      <span class="price">{{ item.dish.price }} ₽</span>
    </div>

    <div class="item-controls">
      <button
        class="quantity-button"
        @click="decrement"
        :disabled="item.quantity <= 1"
      >
        −
      </button>
      <span class="quantity">{{ item.quantity }}</span>
      <button
        class="quantity-button"
        @click="increment"
      >
        +
      </button>

      <button
        class="remove-button"
        @click="$emit('remove', item.dish.id)"
      >
        Удалить
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  item: {
    dish: {
      id: number
      name: string
      description: string
      price: number
    }
    quantity: number
  }
}>()

const emit = defineEmits(['update', 'remove'])

const quantity = ref(props.item.quantity)

const increment = () => {
  quantity.value++
}

const decrement = () => {
  if (quantity.value > 1) {
    quantity.value--
  }
}

watch(quantity, (newVal) => {
  emit('update', props.item.dish.id, newVal)
})
</script>

<style scoped>
.cart-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.item-info {
  flex: 1;
}

.item-info h3 {
  margin: 0 0 0.5rem;
}

.item-info p {
  color: #64748b;
  margin: 0 0 0.5rem;
  font-size: 0.9rem;
}

.price {
  font-weight: bold;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity-button {
  width: 30px;
  height: 30px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.quantity-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity {
  width: 30px;
  text-align: center;
}

.remove-button {
  margin-left: 1rem;
  padding: 0.25rem 0.5rem;
  background: #fef2f2;
  color: #ef4444;
  border: 1px solid #fecaca;
  border-radius: 4px;
  cursor: pointer;
}
</style>