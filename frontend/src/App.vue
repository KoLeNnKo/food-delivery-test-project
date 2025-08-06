<template>
  <div class="app-container">
    <header class="app-header">
      <nav class="app-nav">
        <RouterLink to="/" class="nav-link">Рестораны</RouterLink>
        <RouterLink to="/cart" class="nav-link">Корзина</RouterLink>
        <template v-if="authStore.isAuthenticated">
          <RouterLink to="/profile" class="nav-link">Профиль</RouterLink>
          <button @click="handleLogout" class="nav-button">Выйти</button>
        </template>
        <template v-else>
          <RouterLink to="/auth" class="nav-button">Войти</RouterLink>
        </template>
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

    <footer class="app-footer">
      <p>Food Delivery Service © {{ currentYear }}</p>
    </footer>

    <NotificationContainer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NotificationContainer from '@/components/ui/NotificationContainer.vue'

const authStore = useAuthStore()
const currentYear = ref(new Date().getFullYear())

const handleLogout = async () => {
  try {
    await authStore.logout()
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #3b82f6;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-nav {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.nav-link:hover {
  opacity: 0.8;
}

.nav-link.router-link-active {
  text-decoration: underline;
}

.nav-button {
  margin-left: auto;
  padding: 0.5rem 1rem;
  background: white;
  color: #3b82f6;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  background-color: #1e40af;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style>