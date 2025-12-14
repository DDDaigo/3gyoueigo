from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_login import UserMixin 

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    diaries = db.relationship('Diary', backref='user', lazy=True)

class Diary(db.Model):
    __tablename__ = 'diaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # ★変更: 行ごとのカラムを廃止し、1つのテキストカラムに統一
    original_text = db.Column(db.Text, nullable=False)  # 日本語日記
    translated_text = db.Column(db.Text, nullable=True) # 英語翻訳
    
    # 文法解説 (ここは変更なし)
    grammar_explanation = db.Column(JSONB, nullable=True)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())