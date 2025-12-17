<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="min-h-screen bg-white text-gray-800 font-sans">
    
    <header class="p-6 max-w-3xl mx-auto">
      <div 
        @click="router.push('/')" 
        class="font-bold text-xl text-indigo-600 flex items-center gap-2 cursor-pointer w-fit"
      >
        <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="6" width="12" height="2" rx="1" fill="#4F46E5"/>
          <rect x="4" y="11" width="16" height="2" rx="1" fill="#4F46E5" fill-opacity="0.7"/>
          <rect x="4" y="16" width="10" height="2" rx="1" fill="#4F46E5" fill-opacity="0.4"/>
        </svg>
        3-Line Eigo
      </div>
    </header>

    <main class="max-w-3xl mx-auto px-6 py-10">
      <h1 class="text-3xl font-bold mb-8">プライバシーポリシー</h1>
      
      <div class="space-y-8 text-sm leading-relaxed text-gray-600">
        
        <section>
          <h2 class="text-lg font-bold text-gray-900 mb-3">1. 取得する情報</h2>
          <p>本アプリ（3-Line Eigo）は、サービスの提供にあたり、以下の情報を取得・利用します。</p>
          <ul class="list-disc list-inside mt-2 space-y-1 ml-2">
            <li>Googleアカウント情報（メールアドレス、ユーザーID、表示名）</li>
            <li>ユーザーが入力したテキストデータ（日記の内容）</li>
            <li>Cookie（セッション維持のため）</li>
          </ul>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-900 mb-3">2. 利用目的</h2>
          <p>取得した情報は、以下の目的のために利用されます。</p>
          <ul class="list-disc list-inside mt-2 space-y-1 ml-2">
            <li>本人の確認およびサービスの提供（データの保存・表示）のため</li>
            <li>AI（人工知能）を用いた翻訳および解説生成のため</li>
            <li>サービスの品質向上および不具合対応のため</li>
          </ul>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-900 mb-3">3. 外部サービスへのデータ送信</h2>
          <p>本アプリは、機能実現のために以下の外部サービスを利用しており、必要な範囲でデータを送信します。</p>
          <div class="mt-3 pl-4 border-l-2 border-gray-100">
            <h3 class="font-bold text-gray-800">Google (Firebase / Google Cloud)</h3>
            <p class="mb-2">ユーザー認証およびデータのホスティングに使用します。</p>
            
            <h3 class="font-bold text-gray-800">OpenAI API</h3>
            <p>入力された日記のテキストを翻訳・解説するために使用します。<br>
            ※OpenAIの規定により、API経由で送信されたデータは学習には使用されません（2025年現在）。</p>
          </div>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-900 mb-3">4. 免責事項</h2>
          <p>本アプリのAIによる翻訳・解説の正確性について、完全な保証を行うものではありません。本アプリの利用によって生じた損害について、開発者は一切の責任を負わないものとします。</p>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-900 mb-3">5. お問い合わせ</h2>
          <p>本ポリシーに関するお問い合わせや、データの削除依頼については、以下までご連絡ください。</p>
          <p class="mt-2 font-medium text-indigo-600">
            goosehouse9726@gmail.com
          </p>
        </section>

      </div>

      <div class="mt-12 pt-8 border-t border-gray-100 text-center">
        <button @click="router.back()" class="text-indigo-600 hover:text-indigo-800 font-medium">
          ← 戻る
        </button>
      </div>
    </main>

    <footer class="py-6 text-center text-gray-300 text-xs">
      &copy; 2025 3-Line Eigo.
    </footer>
  </div>
</template>