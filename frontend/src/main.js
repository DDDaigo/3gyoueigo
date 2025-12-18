import './assets/main.css' 
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vue3GoogleLogin from 'vue3-google-login'

import axios from 'axios'
axios.defaults.withCredentials = true

const app = createApp(App)

app.use(router)

//  Google Client IDを設定
// .envファイルで VITE_GOOGLE_CLIENT_ID が設定されている必要があります
app.use(vue3GoogleLogin, {
  // clientId: "131568627154-aji79btmu398hvgc6sl4hke420nojt2o.apps.googleusercontent.com"
  clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID
})

app.mount('#app')


