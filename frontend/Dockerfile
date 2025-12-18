# --- ステージ1: ビルド環境 ---
FROM node:22-alpine as build-stage
WORKDIR /app
COPY package*.json ./

# タイムアウト対策をしたインストールコマンド
RUN npm config set fetch-retry-maxtimeout 600000 \
    && npm config set fetch-retry-mintimeout 10000 \
    && npm install --no-audit --network-timeout=100000

COPY . .

# ★★★ この行が消えていました！これが無いと動きません ★★★
RUN npm run build

# --- ステージ2: 本番環境 (Nginx) ---
FROM nginx:stable-alpine as production
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
