<script setup>
import { useRouter } from 'vue-router' // ★ルーターを使う準備

const router = useRouter()

const startApp = () => {
  // ★ボタンが押されたら /app にページ移動する
  router.push('/app')
}
</script>

<template>
  <div class="min-h-screen bg-white text-gray-800 font-sans">
    
    <header class="p-6 flex justify-between items-center max-w-5xl mx-auto w-full">
      <div class="font-bold text-xl text-indigo-600 flex items-center gap-2">
        <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="6" width="12" height="2" rx="1" fill="#4F46E5"/>
          <rect x="4" y="11" width="16" height="2" rx="1" fill="#4F46E5" fill-opacity="0.7"/>
          <rect x="4" y="16" width="10" height="2" rx="1" fill="#4F46E5" fill-opacity="0.4"/>
        </svg>
        3-line Eigo
      </div>
      <button @click="startApp" class="text-sm font-bold p-2 rounded-full shadow-lg bg-indigo-600 hover:bg-indigo-800 hover:scale-105 text-white transition-colors">
        Start Now
      </button>
    </header>

    <main class="max-w-3xl mx-auto px-6 pt-16 pb-24 text-center">
      <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight text-gray-900 mb-6 leading-tight">
        体験で学ぶ、<br>
        <span class="text-indigo-600">あなただけの</span>英作文。
      </h1>
      
      <p class="text-lg text-gray-500 mb-10 max-w-xl mx-auto leading-relaxed">
        参考書の例文は共感出来なくて覚えられない。<br>
        あなた自身の体験を日本語で綴るだけ。<br>
        AIがあなたの日常を生きた英語に変えます。
      </p>

      <div class="flex flex-col sm:flex-row justify-center gap-4">
        <button 
          @click="startApp"
          class="bg-indigo-600 text-white px-8 py-4 rounded-full font-bold text-lg shadow-lg hover:bg-indigo-700 hover:scale-105 transition-all flex items-center justify-center gap-2"
        >
          <span>今すぐ使ってみる</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
        </button>
      </div>
      
      <p class="mt-4 text-xs text-gray-400">登録不要・完全無料</p>
    </main>

    <section class="bg-gray-50 py-20 border-t border-gray-100">
      <div class="max-w-5xl mx-auto px-6">
        <div class="grid md:grid-cols-3 gap-10 text-center">
          
          <div class="space-y-4">
            <div class="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mx-auto text-2xl">
              ✍️
            </div>
            <h3 class="font-bold text-xl">1. 日本語で書く</h3>
            <p class="text-gray-500 text-sm leading-relaxed">
              英語にする必要はありません。<br>日記のように日本語で入力します。
            </p>
          </div>

          <div class="space-y-4">
            <div class="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mx-auto text-2xl">
              ✨
            </div>
            <h3 class="font-bold text-xl">2. AIが翻訳</h3>
            <p class="text-gray-500 text-sm leading-relaxed">
              瞬時に自然な英語へ翻訳。<br>教科書にはない、あなたの言葉です。
            </p>
          </div>

          <div class="space-y-4">
            <div class="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mx-auto text-2xl">
              💡
            </div>
            <h3 class="font-bold text-xl">3. 解説で学ぶ</h3>
            <p class="text-gray-500 text-sm leading-relaxed">
              なぜその表現になるのか？<br>AIが文法ポイントを解説します。
            </p>
          </div>

        </div>
      </div>
    </section>

    <footer class="py-10 text-center text-gray-300 text-xs flex flex-col gap-2">
      <div>&copy; 2025 3-Line Eigo.</div>
      <router-link to="/privacy" class="hover:text-gray-500 transition-colors underline decoration-gray-200 underline-offset-2">
        プライバシーポリシー
      </router-link>
    </footer>
  </div>
</template>