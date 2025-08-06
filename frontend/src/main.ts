import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// Инициализация приложения
const app = createApp(App)

// Плагины
app.use(createPinia())
app.use(router)
app.use(VueQueryPlugin)

// Глобальные компоненты
app.component('Spinner', () => import('@/components/ui/Spinner.vue'))

// Конфигурация VueQuery
VueQueryPlugin.install(app, {
  queryClientConfig: {
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        retry: 1,
        staleTime: 1000 * 60 * 5 // 5 минут
      }
    }
  }
})

app.mount('#app')