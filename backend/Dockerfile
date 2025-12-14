# ベースイメージ
FROM python:3.11-slim as base

# 作業ディレクトリ
WORKDIR /app

# システム依存パッケージのインストール (PostgreSQL接続用など)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 依存ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- 開発用ステージ (target: development) ---
FROM base as development
# 環境変数を設定 (Flaskのデバッグモード有効化)
ENV FLASK_DEBUG=1
# ホスト0.0.0.0で起動しないとコンテナ外からアクセスできない
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# --- 本番用ステージ (target: production) ---
FROM base as production
COPY . .
# 本番はGunicornで起動
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]