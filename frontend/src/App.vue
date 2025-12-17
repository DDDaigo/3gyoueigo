<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router' // ★useRoute, useRouterを追加
import { ref, onMounted, watch } from 'vue' // ★watchを追加
import axios from 'axios'
import GoogleLoginComponent from './components/GoogleLogin.vue'

const api = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'
const route = useRoute()   // ★現在のURL情報を取得
const router = useRouter() // ★ページ移動用

const isLoggedIn = ref(false)
const userName = ref('')

// ログインチェック関数
const checkLoginStatus = async () => {
  try {
    const response = await axios.get(`${api}/api/auth/me`, { 
      withCredentials: true 
    })
    
    if (response.data.is_logged_in) {
      isLoggedIn.value = true
      userName.value = response.data.user.name
      
      // ★追加: ログイン済みで、今トップページ(LP)にいるなら、自動でアプリ(/app)に飛ばす
      if (route.path === '/') {
        router.push('/app')
      }
    } else {
      isLoggedIn.value = false
      userName.value = ''
    }
  } catch (error) {
    console.error('ログインチェック失敗', error)
    isLoggedIn.value = false
  }
}

const handleLoginSuccess = (data) => {
  isLoggedIn.value = true
  userName.value = data.user.name
  // ログインしたらアプリ画面へ移動
  router.push('/app')
}

const logout = async () => {
  try {
    await axios.post(`${api}/api/auth/logout`, {}, { 
      withCredentials: true 
    })
    isLoggedIn.value = false
    userName.value = ''
    // ログアウトしたらLPに戻す
    router.push('/')
  } catch (error) {
    console.error('ログアウト失敗', error)
    isLoggedIn.value = false
    router.push('/')
  }
}

onMounted(() => {
  checkLoginStatus()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-800 font-sans">
    
    <header v-if="route.path !== '/'" class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-2xl mx-auto px-4 h-16 flex items-center justify-between">
        <h1 @click="router.push('/app')" class="text-xl font-bold text-indigo-600 tracking-wider flex items-center gap-2 cursor-pointer">
          <span>📝</span> 3-Line Eigo
        </h1>
        
        <div v-if="isLoggedIn" class="flex items-center gap-4">
          <span class="text-sm text-gray-600 hidden sm:inline">Hello, {{ userName }}</span>
          <button @click="logout" class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-600 px-3 py-1.5 rounded-lg transition-colors">
            ログアウト
          </button>
        </div>
        
        <div v-else>
          <GoogleLoginComponent @login-success="handleLoginSuccess" />
        </div>
      </div>
    </header>

    <div v-if="route.path !== '/' && !isLoggedIn" class="bg-blue-50 border-b border-blue-100 px-4 py-3">
      <div class="max-w-2xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-blue-800">
        <div class="flex items-center gap-2">
          <span class="text-lg">💡</span>
          <p>現在は<strong>お試しモード</strong>です。ページを閉じると履歴は消えます。</p>
        </div>
      </div>
    </div>

    <main :class="{ 'max-w-2xl mx-auto px-4 py-6': route.path !== '/' }">
      <RouterView />
    </main>
  </div>
</template>