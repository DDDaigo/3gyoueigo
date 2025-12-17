import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LandingView from '../views/LandingView.vue' // ★LPをインポート
import PrivacyPolicyView from '../views/PrivacyPolicyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView // ★トップページはLPにする
    },
    {
      path: '/app', // ★アプリ本体は /app という住所に移す
      name: 'home',
      component: HomeView
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyPolicyView
    }    
  ]
})

export default router