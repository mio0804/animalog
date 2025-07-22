from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cognito_sub = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーションシップ
    pets = db.relationship('Pet', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    diaries = db.relationship('Diary', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50))
    breed = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーションシップ
    diaries = db.relationship('Diary', backref='pet', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'diary_count': self.diaries.count()
        }

class Diary(db.Model):
    __tablename__ = 'diaries'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = db.Column(UUID(as_uuid=True), db.ForeignKey('pets.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        from flask import current_app
        
        # USE_S3が有効な場合、ローカル画像URLをプロキシURLに変換
        image_url = self.image_url
        if image_url and current_app.config.get('USE_S3', False):
            if image_url.startswith('/uploads/'):
                # ローカルパスからファイル名を抽出し、プロキシエンドポイントを使用
                filename = image_url.replace('/uploads/', '')
                image_url = f"/api/images/proxy/{filename}"
            elif 's3.amazonaws.com' in image_url or 's3.ap-northeast-1.amazonaws.com' in image_url:
                # S3 URLからファイル名を抽出し、プロキシエンドポイントを使用
                parts = image_url.split('/')
                filename = parts[-1]
                image_url = f"/api/images/proxy/{filename}"
        
        return {
            'id': str(self.id),
            'pet_id': str(self.pet_id),
            'pet_name': self.pet.name,
            'title': self.title,
            'content': self.content,
            'image_url': image_url,
            'created_at': self.created_at.isoformat()
        }