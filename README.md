📝 3-Line Eigo (3行えいご)
体験で学ぶ、あなただけの英作文。

「3-Line Eigo」は、日々の出来事を日本語で記録するだけで、AIが自然な英語に翻訳し、文法解説を行ってくれる英語学習Webアプリケーションです。 教科書の例文ではなく、**「自分の人生（リアルな日常）」**を教材にすることで、記憶に残る英語学習体験を提供します。

✨ 主な機能
日記投稿: 日本語で今日あったことを入力（3行程度を推奨）。

AI翻訳 & 解説: OpenAI APIを使用し、自然な英語への翻訳と、重要な文法ポイントの解説を自動生成。

チャット風UI: LINEのような親しみやすいインターフェースで、過去の投稿を振り返りやすく設計。

Googleログイン: Googleアカウントを使用したセキュアな認証（OAuth 2.0）。

データ保存: ユーザーごとの日記データをデータベース（PostgreSQL）に永続化。

直感的な操作: 長押しによる削除機能、未ログイン時のお試しモードなど。

🛠 使用技術 (Tech Stack)
Frontend
Framework: Vue.js 3 (Composition API)

Build Tool: Vite

Styling: Tailwind CSS

Router: Vue Router

HTTP Client: Axios

Backend
Language: Python 3.9+

Framework: Flask

ORM: SQLAlchemy

Auth: Authlib (Google OAuth)

AI: OpenAI API (GPT-3.5/4)

Infrastructure & Database
Database: PostgreSQL

Container: Docker / Docker Compose

Environment: Nginx (予定), Gunicorn (予定)

🚀 環境構築 (Local Development)
Dockerを使用しているため、コマンド一つで環境を立ち上げることが可能です。

1. リポジトリのクローン
Bash

git clone https://github.com/DDDaigo/3gyoueigo.git
cd 3gyoueigo
2. 環境変数の設定
ルートディレクトリに .env ファイルを作成し、以下の変数を設定してください。

Ini, TOML

# .env

# Flask設定
SECRET_KEY=your_secret_key_here
FLASK_APP=app.py
FLASK_ENV=development

# データベース設定
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=3gyou_dev_db
DATABASE_URL=postgresql://user:password@db:5432/3gyou_dev_db

# OpenAI API設定
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# Google OAuth設定
GOOGLE_CLIENT_ID=xxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxxxxxxxxxxxx
3. アプリケーションの起動
Docker Composeを使用してコンテナをビルド・起動します。

Bash

docker-compose -f docker-compose.dev.yml up --build
起動後、以下のURLでアクセスできます。

Frontend: http://localhost:5173

Backend API: http://localhost:5000

4. データベースの初期化（初回のみ）
コンテナ起動後、以下のコマンドでテーブルを作成します。

Bash

docker-compose -f docker-compose.dev.yml exec backend python -c "from app import db; db.create_all()"
📂 ディレクトリ構成
3gyoueigo/
├── backend/            # Flask APIサーバー
│   ├── app.py          # メインアプリケーション
│   ├── models.py       # DBモデル定義
│   └── requirements.txt
├── frontend/           # Vue.js フロントエンド
│   ├── src/
│   │   ├── views/      # 各ページコンポーネント
│   │   ├── components/ # 共通パーツ
│   │   └── router/     # ルーティング定義
│   └── index.html
├── docker-compose.dev.yml # 開発用Docker設定
└── README.md
🔒 プライバシーポリシー
本アプリはGoogle認証を使用し、ユーザーのメールアドレスとプロフィール名を取得しますが、認証およびアプリ内での表示以外の目的には使用しません。 入力された日記データはOpenAI APIへ送信されますが、学習データとしての利用はオプトアウトされています。

👤 Author
Created by DDDaigo