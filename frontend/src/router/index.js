import { createRouter, createWebHistory } from 'vue-router'
// 先ほど作った HomeView.vue をインポート
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    // Aboutページなどは一旦消しておきます
  ]
})

export default router