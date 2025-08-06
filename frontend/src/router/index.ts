import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.token) {
    next('/auth')
  } else {
    next()
  }
})

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
        title: 'Рестораны'
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('@/views/AuthView.vue')
  },
  {
    path: '/restaurants/:id',
    name: 'restaurant',
    component: () => import('@/views/RestaurantView.vue')
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('@/views/CartView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router