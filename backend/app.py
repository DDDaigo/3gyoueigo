import os
import json
from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Diary
from openai import OpenAI
from datetime import datetime

# ★追加: Googleトークン検証用ライブラリ
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

app = Flask(__name__)

# --- 設定 ---
app.secret_key = "super_secret_key_for_dev"
app.config['SESSION_COOKIE_NAME'] = 'my_app_session'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# CORS (Cookieを通す設定)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:8081", "http://localhost:8081"])

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ルート定義 ---

@app.route('/')
def index():
    return "3gyoueigo Backend is running!"

# ★変更点: Googleログイン処理 (POSTでトークンを受け取るだけ)
@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    import traceback # エラー詳細を見るために追加
    
    print("\n=== Google Auth Start ===", flush=True)
    
    try:
        data = request.json
        token = data.get('credential')
        
        # 1. 環境変数の確認
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        print(f"★ Client ID in Backend: {client_id}", flush=True)
        
        if not client_id:
            print("ERROR: GOOGLE_CLIENT_ID is missing in Backend .env", flush=True)
            return jsonify({"error": "Backend configuration error"}), 500

        if not token:
            print("ERROR: Token is missing from Frontend", flush=True)
            return jsonify({"error": "Token is missing"}), 400

        # 2. 検証開始
        print("★ Verifying token...", flush=True)
        id_info = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            client_id
        )
        print("★ Token Verified!", flush=True)

        # 3. ユーザー情報取得
        google_id = id_info['sub']
        email = id_info['email']
        name = id_info.get('name', '')
        print(f"★ User: {email}", flush=True)

        # 4. DB保存
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            print("★ Creating new user...", flush=True)
            user = User(google_id=google_id, email=email, name=name)
            db.session.add(user)
            db.session.commit()
        else:
            print("★ User exists.", flush=True)

        # 5. ログイン
        login_user(user)
        print("=== Login Successful ===\n", flush=True)
        
        return jsonify({"message": "Login successful", "user": {"name": name, "email": email}}), 200

    except ValueError as e:
        # トークン不正（期限切れや偽物）
        print(f"!!! ValueError (Token Invalid) !!!: {e}", flush=True)
        return jsonify({"error": "Invalid token"}), 401
        
    except Exception as e:
        # ★ここで500エラーの正体を暴きます
        print(f"\n!!! CRITICAL ERROR (500) !!!", flush=True)
        print(f"Error Type: {type(e).__name__}", flush=True)
        print(f"Error Message: {e}", flush=True)
        print(traceback.format_exc(), flush=True) # 詳細なエラーログ
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200

@app.route('/api/auth/me')
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            "is_logged_in": True,
            "user": {"name": current_user.name, "email": current_user.email}
        })
    else:
        return jsonify({"is_logged_in": False})

# --- 日記機能 (そのまま) ---
@app.route('/api/diaries', methods=['GET'])
def get_diaries():
    if not current_user.is_authenticated:
        return jsonify({"data": []}), 200
    
    user_id = current_user.id
    diaries = Diary.query.filter_by(user_id=user_id).order_by(Diary.date.asc(), Diary.created_at.asc()).all()
    results = [{"id": d.id, "date": d.date.strftime('%Y-%m-%d'), "original_text": d.original_text, "translated_text": d.translated_text, "grammar": d.grammar_explanation} for d in diaries]
    return jsonify({"data": results}), 200

@app.route('/api/diaries', methods=['POST'])
def create_diary():
    # 1. データを受け取る
    data = request.json
    date_str = data.get('date')
    content = data.get('content', '')

    # 2. バリデーション
    if not content:
        return jsonify({"error": "日記が入力されていません"}), 400
    if len(content) > 200:
        return jsonify({"error": "200文字以内で入力してください"}), 400

    # 3. AIによる翻訳と解説（プロンプト作成）
    prompt = f"""
    以下の日本語の日記を自然な英語に翻訳し、
    英語学習者の日本人向けに、重要な文法ポイントを【日本語で】解説してください。
    
    日記本文:
    {content}
    
    以下のJSONフォーマットのみで出力してください。Markdownは不要です。
    {{
        "translation": "英文翻訳結果",
        "explanations": [
            {{"point": "文法項目", "detail": "詳しい解説(必ず日本語)"}},
            {{"point": "...", "detail": "..."}}
        ]
    }}
    """

    try:
        # 4. OpenAI APIを呼び出す
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは日本人の英語学習者をサポートする先生です。解説は必ず日本語で行ってください。出力はJSON形式です。"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # 5. 結果を解析
        ai_content = response.choices[0].message.content
        ai_data = json.loads(ai_content)
        
        # 6. ログインしていればDBに保存
        if current_user.is_authenticated:
            new_diary = Diary(
                user_id=current_user.id,
                date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                original_text=content,
                translated_text=ai_data.get("translation"),
                grammar_explanation=ai_data.get("explanations", [])
            )
            db.session.add(new_diary)
            db.session.commit()
            print("DBに保存しました", flush=True)
        else:
            print("未ログインのため保存しませんでした", flush=True)
        
        return jsonify({"message": "Diary processed!", "data": ai_data}), 201

    except Exception as e:
        print(f"Error in create_diary: {e}", flush=True)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/diaries/<int:diary_id>', methods=['DELETE'])
@login_required
def delete_diary(diary_id):
    # 1. 削除対象の日記を探す
    diary = Diary.query.get(diary_id)
    
    # 2. 日記がない、または他人の日記ならエラー
    if not diary:
        return jsonify({"error": "Diary not found"}), 404
    if diary.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    # 3. 削除実行
    db.session.delete(diary)
    db.session.commit()
    
    return jsonify({"message": "Deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)