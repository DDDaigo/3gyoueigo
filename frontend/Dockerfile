# ベースイメージ
FROM node:20-alpine as base

WORKDIR /app

# パッケージ定義をコピー
COPY package*.json ./

# --- 開発用ステージ (target: development) ---
FROM base as development
RUN npm install
COPY . .
# Viteの開発サーバー起動 (--host オプション必須)
CMD ["npm", "run", "dev", "--", "--host"]

# --- 本番用ステージ (target: production) ---
FROM base as production
RUN npm install
COPY . .
RUN npm run build
# 本番運用時はここでNginxなどにファイルを渡す処理が入りますが、
# いったんビルド確認用にここまでとします