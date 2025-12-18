<template>
  <div class="flex justify-center">
    <GoogleLogin :callback="callback" />
  </div>
</template>

<script setup>
import { GoogleLogin } from 'vue3-google-login'
import axios from 'axios'

const emit = defineEmits(['login-success'])
// APIのURL（環境変数が読めないときのための保険で直書き）
const api = import.meta.env.VITE_API_URL

const callback = async (response) => {
  // ★ログ確認: 今度こそ "credential" が入っているはずです
  console.log("Google認証成功(Vue側):", response)

  // credential がない場合は処理しない（codeが返ってきた場合などの対策）
  if (!response.credential) {
    console.error("エラー: credentialがありません。response:", response)
    return
  }

  try {
    const res = await axios.post(`${api}/api/auth/google`, {
      credential: response.credential
    }, { 
      withCredentials: true 
    })

    if (res.status === 200) {
      console.log("バックエンドログイン成功")
      emit('login-success', res.data)
    }
  } catch (err) {
    console.error('バックエンドログイン失敗:', err)
    alert("ログイン処理に失敗しました")
  }
}
</script>
