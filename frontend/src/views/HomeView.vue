<script setup>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'

// ★修正: 環境変数が読み込めない場合の「保険」として、初期値を設定します
const api = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

// 入力中の日記
const diaryContent = ref('')
const isAnalyzing = ref(false)
const diaries = ref([])

const fetchDiaries = async () => {
  try {
    // ★修正1: URLを変数にし、{ withCredentials: true } を追加
    // これがないと「ログインしている」という情報(Cookie)がサーバーに届きません
    const response = await axios.get(`${api}/api/diaries`, { 
      withCredentials: true 
    })
    
    diaries.value = response.data.data
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('日記の読み込みに失敗しました', error)
  }
}

const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

onMounted(() => {
  fetchDiaries()
})

const submitDiary = async () => {
  if (!diaryContent.value) return
  if (diaryContent.value.length > 200) {
    alert('200文字以内で入力してください')
    return
  }

  isAnalyzing.value = true
  
  try {
    const today = new Date().toISOString().split('T')[0]

    const response = await axios.post(`${api}/api/diaries`, {
      date: today,
      content: diaryContent.value
    }, {
      withCredentials: true
    })

    const newDiaryData = response.data.data
    
    diaries.value.push({
      id: Date.now(),
      date: today,
      original_text: diaryContent.value,
      translated_text: newDiaryData.translation,
      grammar: newDiaryData.explanations 
    })

    diaryContent.value = ''
    await nextTick()
    scrollToBottom()

  } catch (error) {
    console.error(error)
    alert('エラーが発生しました。')
  } finally {
    isAnalyzing.value = false
  }
}
</script>

<template>
  <div class="space-y-6 pb-32">
    <div class="space-y-8">
      <div v-if="diaries.length === 0" class="text-center text-gray-400 py-10">
        まだ日記はありません。<br>今日あったことを書いてみましょう！
      </div>

      <div v-for="(diary, index) in diaries" :key="diary.id" class="flex flex-col gap-2">
        <div v-if="index === 0 || diaries[index - 1].date !== diary.date" class="flex justify-center mt-4 mb-2">
          <span class="bg-gray-200 text-gray-600 text-xs px-3 py-1 rounded-full shadow-sm">
            {{ diary.date }}
          </span>
        </div>
        
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 mx-2">
          <p class="text-gray-800 mb-3 leading-relaxed whitespace-pre-wrap">{{ diary.original_text }}</p>
          <div class="border-t border-gray-100 pt-3">
            <p class="text-indigo-700 font-medium mb-1">{{ diary.translated_text }}</p>
            <div v-if="diary.grammar && diary.grammar.length > 0" class="mt-3 bg-indigo-50 p-3 rounded-lg text-sm">
              <p class="font-bold text-indigo-800 mb-2">💡 文法ポイント</p>
              <ul class="list-disc list-inside space-y-1 text-gray-700">
                <li v-for="(exp, i) in diary.grammar" :key="i">
                  <span class="font-semibold">{{ exp.point }}</span>: {{ exp.detail }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 p-4 pb-8 z-10">
      <div class="max-w-2xl mx-auto flex gap-2">
        <textarea 
          v-model="diaryContent"
          placeholder="今日はどんな1日でしたか？(200文字以内)"
          class="flex-1 bg-gray-100 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none h-16"
        ></textarea>
        <button 
          @click="submitDiary"
          :disabled="isAnalyzing"
          class="bg-indigo-600 text-white px-6 rounded-xl font-bold hover:bg-indigo-700 disabled:bg-gray-300 transition-colors flex items-center justify-center min-w-[80px]"
        >
          <span v-if="isAnalyzing" class="animate-spin text-xl">↻</span>
          <span v-else>送信</span>
        </button>
      </div>
    </div>
  </div>
</template>