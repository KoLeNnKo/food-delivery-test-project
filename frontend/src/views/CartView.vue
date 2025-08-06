<template>
  <div class="cart-view">
    <h1>Корзина</h1>

    <div v-if="cartStore.isEmpty" class="empty-cart">
      <p>Ваша корзина пуста</p>
      <RouterLink to="/" class="back-button">
        Вернуться к ресторанам
      </RouterLink>
    </div>

    <div v-else>
      <!-- Список товаров -->
      <div class="cart-items">
        <CartItem
          v-for="item in cartStore.items"
          :key="item.dish.id"
          :item="item"
          @update="updateQuantity"
          @remove="removeItem"
        />
      </div>

      <!-- Итого -->
      <div class="cart-summary">
        <div class="summary-row">
          <span>Сумма:</span>
          <span>{{ cartStore.total }} ₽</span>
        </div>
        <div class="summary-row">
          <span>Доставка:</span>
          <span>{{ deliveryPrice }} ₽</span>
        </div>
        <div class="summary-row total">
          <span>Итого:</span>
          <span>{{ cartStore.total + deliveryPrice }} ₽</span>
        </div>

        <button
          class="checkout-button"
          @click="handleCheckout"
          :disabled="isProcessing"
        >
          <span v-if="!isProcessing">Оформить заказ</span>
          <Spinner v-else />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import CartItem from '@/components/CartItem.vue'
import Spinner from '@/components/ui/Spinner.vue'

const router = useRouter()
const cartStore = useCartStore()
const isProcessing = ref(false)
const deliveryPrice = 150 // Фиксированная стоимость доставки

const updateQuantity = (dishId: number, quantity: number) => {
  cartStore.updateItem(dishId, quantity)
}

const removeItem = (dishId: number) => {
  cartStore.removeItem(dishId)
}

const handleCheckout = async () => {
  try {
    isProcessing.value = true
    await cartStore.checkout()
    router.push('/orders')
  } catch (error) {
    alert('Ошибка при оформлении заказа')
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped>
.cart-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.empty-cart {
  text-align: center;
  padding: 2rem;
}

.empty-cart p {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.back-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border-radius: 4px;
  text-decoration: none;
}

.cart-items {
  margin-bottom: 2rem;
}

.cart-summary {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.summary-row.total {
  font-weight: bold;
  font-size: 1.1rem;
  margin: 1rem 0;
}

.checkout-button {
  width: 100%;
  padding: 1rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
}

.checkout-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>