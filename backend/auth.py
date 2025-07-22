from functools import wraps
from flask import request, jsonify, current_app
from jose import jwt, JWTError
from datetime import datetime
import requests
from models import User, db

def get_current_user():
    """Get current user from token or mock user in development"""
    if not current_app.config['USE_COGNITO']:
        # 開発モード - モックユーザーを使用
        mock_sub = current_app.config['MOCK_USER_ID']
        user = User.query.filter_by(cognito_sub=mock_sub).first()
        if not user:
            user = User(
                cognito_sub=mock_sub,
                email=current_app.config['MOCK_USER_EMAIL'],
                username=current_app.config['MOCK_USER_NAME']
            )
            db.session.add(user)
            db.session.commit()
        return user
    
    # 本番モード - Cognitoトークンを検証
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    user_info = verify_cognito_token(token)
    if not user_info:
        return None
    
    # ユーザーを検索または作成
    user = User.query.filter_by(cognito_sub=user_info['sub']).first()
    if not user:
        user = User(
            cognito_sub=user_info['sub'],
            email=user_info.get('email', ''),
            username=user_info.get('name', user_info.get('email', '').split('@')[0])
        )
        db.session.add(user)
        db.session.commit()
    
    return user

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function

def verify_cognito_token(token):
    """Verify Cognito JWT token"""
    try:
        # Cognito公開鍵を取得
        region = current_app.config['COGNITO_REGION']
        user_pool_id = current_app.config['COGNITO_USER_POOL_ID']
        keys_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
        
        response = requests.get(keys_url)
        keys = response.json()['keys']
        
        # トークンヘッダをデコードしてkidを取得
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        
        # 正しいキーを検索
        key = next((k for k in keys if k['kid'] == kid), None)
        if not key:
            return None
        
        # トークンを検証してデコード
        payload = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=current_app.config['COGNITO_APP_CLIENT_ID']
        )
        
        # トークンの有効期限を検証
        if datetime.fromtimestamp(payload['exp']) < datetime.utcnow():
            return None
        
        return payload
        
    except (JWTError, KeyError, requests.RequestException):
        return None