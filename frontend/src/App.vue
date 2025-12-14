<script setup>
import { RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import GoogleLoginComponent from './components/GoogleLogin.vue'

// ★修正1: URLが読み込めない時のための保険 (fallback) を入れます
const api = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const isLoggedIn = ref(false)
const userName = ref('')

const checkLoginStatus = async () => {
  try {
    // ★修正2: 変数 api を使い、withCredentials: true を入れます
    const response = await axios.get(`${api}/api/auth/me`, { 
      withCredentials: true 
    })
    
    if (response.data.is_logged_in) {
      isLoggedIn.value = true
      userName.value = response.data.user.name
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
  // ログイン成功時にリロードしてデータを再取得させる
  window.location.reload()
}

const logout = async () => {
  try {
    // ★修正3: ここも変数 api を使い、withCredentials: true を入れます
    await axios.post(`${api}/api/auth/logout`, {}, { 
      withCredentials: true 
    })
    isLoggedIn.value = false
    userName.value = ''
    window.location.reload()
  } catch (error) {
    console.error('ログアウト失敗', error)
    // 失敗しても画面上はログアウト扱いにした方が親切です
    isLoggedIn.value = false
    window.location.reload()
  }
}

onMounted(() => {
  checkLoginStatus()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-800 font-sans">
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-2xl mx-auto px-4 h-16 flex items-center justify-between">
        <h1 class="text-xl font-bold text-indigo-600 tracking-wider flex items-center gap-2">
          <span>📝</span> 3行えいご
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

    <div v-if="!isLoggedIn" class="bg-blue-50 border-b border-blue-100 px-4 py-3">
      <div class="max-w-2xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-blue-800">
        <div class="flex items-center gap-2">
          <span class="text-lg">💡</span>
          <p>現在は<strong>お試しモード</strong>です。ページを閉じると履歴は消えます。</p>
        </div>
        <GoogleLoginComponent @login-success="handleLoginSuccess" />
      </div>
    </div>

    <main class="max-w-2xl mx-auto px-4 py-6">
      <RouterView />
    </main>
  </div>
</template>