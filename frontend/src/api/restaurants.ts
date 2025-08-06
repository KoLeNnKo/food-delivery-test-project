import axios from 'axios'

export const getRestaurants = () => {
  return axios.get('/restaurants')
}

export const getCategories = () => {
  return axios.get('/categories')
}

export const getRestaurantById = (id: number) => {
  return axios.get(`/restaurants/${id}`)
}