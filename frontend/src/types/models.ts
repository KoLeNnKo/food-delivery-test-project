// Базовые типы
export type ID = number | string

// Пользователь
export interface User {
  id: ID
  email: string
  role: 'customer' | 'courier' | 'admin'
  phone?: string
  address?: string
  createdAt: string
}

// Ресторан
export interface Restaurant {
  id: ID
  name: string
  description: string
  rating: number
  delivery_time: string
  image: string
  categories: Category[]
  menu: Dish[]
  location: {
    lat: number
    lng: number
  }
}

// Категория ресторана/блюда
export interface Category {
  id: ID
  name: string
  icon?: string
}

// Блюдо
export interface Dish {
  id: ID
  name: string
  description: string
  price: number
  image?: string
  category: Category
  weight?: string
  ingredients?: string[]
  is_available: boolean
}

// Позиция в корзине
export interface CartItem {
  dish: Dish
  quantity: number
  selectedOptions?: {
    id: ID
    name: string
    price: number
  }[]
}

// Заказ
export interface Order {
  id: ID
  user_id: ID
  restaurant_id: ID
  status: 'created' | 'paid' | 'cooking' | 'delivering' | 'delivered' | 'canceled'
  total: number
  items: OrderItem[]
  created_at: string
  delivered_at?: string
  courier_id?: ID
  address: string
  phone: string
  comment?: string
}

// Позиция в заказе
export interface OrderItem {
  id: ID
  dish_id: ID
  order_id: ID
  quantity: number
  price_at_order: number
  dish: Dish
}

// Формы
export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm extends LoginForm {
  confirmPassword: string
}

export interface ProfileForm {
  email: string
  phone: string
  address: string
}

export interface PasswordChangeForm {
  currentPassword: string
  newPassword: string
  confirmPassword: string
}

// API Responses
export interface ApiResponse<T> {
  data: T
  message?: string
  errors?: Record<string, string[]>
}

export interface PaginatedResponse<T> {
  data: T[]
  meta: {
    total: number
    per_page: number
    current_page: number
    last_page: number
  }
}

// Состояния хранилищ
export interface AuthState {
  user: User | null
  token: string | null
}

export interface CartState {
  items: CartItem[]
  restaurantId?: ID
}

export interface RestaurantsState {
  list: Restaurant[]
  current?: Restaurant
  categories: Category[]
  isLoading: boolean
  error: string | null
}

// Полезные типы
export type Optional<T, K extends keyof T> = Pick<Partial<T>, K> & Omit<T, K>
export type RequireFields<T, K extends keyof T> = T & Required<Pick<T, K>>