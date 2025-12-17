<script setup>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'

// 環境変数の読み込み
const api = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

// 状態管理
const diaryContent = ref('')
const isAnalyzing = ref(false)
const diaries = ref([])
const activeDeleteId = ref(null) // 削除モード中のID
let longPressTimer = null // 長押しタイマー

// --- 削除・長押し関連ロジック ---

const startLongPress = (id) => {
  if (activeDeleteId.value) return // 既にモード中なら無視

  longPressTimer = setTimeout(() => {
    // 0.8秒後に削除モードON
    if (navigator.vibrate) navigator.vibrate(50) // スマホならブルッとさせる
    activeDeleteId.value = id
  }, 800)
}

const cancelLongPress = () => {
  if (longPressTimer) {
    clearTimeout(longPressTimer)
    longPressTimer = null
  }
}

const resetDeleteMode = () => {
  activeDeleteId.value = null
}

const deleteDiary = async (id) => {

  try {
    await axios.delete(`${api}/api/diaries/${id}`, { 
      withCredentials: true 
    })
    diaries.value = diaries.value.filter(d => d.id !== id)
    activeDeleteId.value = null
  } catch (error) {
    console.error('削除失敗:', error)
    alert('削除できませんでした')
  }
}

// --- 日記読み込み・送信ロジック ---

const fetchDiaries = async () => {
  try {
    const response = await axios.get(`${api}/api/diaries`, { 
      withCredentials: true 
    })
    diaries.value = response.data.data || []
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
      id: Date.now(), // 一時的なID
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

onMounted(() => {
  fetchDiaries()
})
</script>

<template>
  <div class="space-y-6 pb-32 relative min-h-screen">
    
    <div 
      v-if="activeDeleteId" 
      class="fixed inset-0 z-40 bg-black/20 backdrop-blur-[1px] transition-all"
      @click="resetDeleteMode"
    ></div>

    <div class="space-y-8 px-2 pt-4">
      <div v-if="diaries.length === 0" class="text-center text-gray-400 py-10">
        まだ日記はありません。<br>今日あったことを書いてみましょう！
      </div>

      <div v-for="(diary, index) in diaries" :key="diary.id" class="flex flex-col gap-2 relative">
        
        <div v-if="index === 0 || diaries[index - 1].date !== diary.date" class="flex justify-center mt-4 mb-2">
          <span class="bg-gray-200 text-gray-600 text-xs px-3 py-1 rounded-full shadow-sm">
            {{ diary.date }}
          </span>
        </div>
        
        <div 
          class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 mx-1 transition-all duration-300 select-none relative"
          :class="{ 
            'scale-105 shadow-xl ring-2 ring-indigo-200 z-50': activeDeleteId === diary.id,
            'z-0': activeDeleteId !== diary.id
          }"
          @mousedown="startLongPress(diary.id)"
          @touchstart="startLongPress(diary.id)"
          @mouseup="cancelLongPress"
          @mouseleave="cancelLongPress"
          @touchend="cancelLongPress"
        >
          
          <button
            v-if="activeDeleteId === diary.id"
            @click.stop="deleteDiary(diary.id)"
            class="absolute -top-3 -right-3 bg-red-500 text-white p-2 rounded-full shadow-lg hover:bg-red-600 transition-colors animate-bounce z-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>
          </button>

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

    <div class="fixed bottom-0 left-0 w-full bg-white/90 backdrop-blur-sm border-t border-gray-200 p-4 pb-8 z-30">
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