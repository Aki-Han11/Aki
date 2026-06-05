import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCart as fetchCart } from '../api/endpoints'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const count = ref(0)

  async function fetch() {
    try {
      const res = await fetchCart()
      items.value = res.data
      count.value = res.data.length
    } catch (e) {
      items.value = []
      count.value = 0
    }
  }

  return { items, count, fetch }
})
