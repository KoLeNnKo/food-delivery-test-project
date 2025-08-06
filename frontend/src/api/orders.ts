import axios from 'axios'

export const createOrder = (orderData: {
  user_id: number
  items: Array<{
    dish_id: number
    quantity: number
  }>
}) => {
  return axios.post('/orders', orderData)
}

export const getOrderHistory = (userId: number) => {
  return axios.get(`/users/${userId}/orders`)
}