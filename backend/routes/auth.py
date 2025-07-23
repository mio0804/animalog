from flask import Blueprint, jsonify, request, current_app, redirect
from auth import get_current_user
import requests
import secrets
import base64
from urllib.parse import urlencode
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/me', methods=['GET'])
def get_me():
    """現在のユーザー情報を取得"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({'user': user.to_dict()})

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """ログインエンドポイント - 開発モードではモックトークンを返す"""
    if not current_app.config['USE_COGNITO']:
        # 開発モード - モックトークンを返す
        return jsonify({
            'token': 'mock-development-token',
            'user': {
                'id': current_app.config['MOCK_USER_ID'],
                'email': current_app.config['MOCK_USER_EMAIL'],
                'username': current_app.config['MOCK_USER_NAME']
            }
        })
    
    # 本番モード - CognitoホストUIへのリダイレクトURLを返す
    cognito_domain = current_app.config['COGNITO_DOMAIN']
    client_id = current_app.config['COGNITO_APP_CLIENT_ID']
    redirect_uri = current_app.config['COGNITO_REDIRECT_URI']
    
    auth_url = f"https://{cognito_domain}/login?" + urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile'
    })
    
    return jsonify({
        'auth_url': auth_url
    })

@auth_bp.route('/api/auth/callback', methods=['POST'])
def callback():
    """Cognitoからの認証コールバックを処理"""
    if not current_app.config['USE_COGNITO']:
        return jsonify({'error': 'Cognito is not enabled'}), 400
    
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({'error': 'Authorization code required'}), 400
    
    # 認証コードをトークンに交換
    token_endpoint = f"https://{current_app.config['COGNITO_DOMAIN']}/oauth2/token"
    client_id = current_app.config['COGNITO_APP_CLIENT_ID']
    client_secret = current_app.config['COGNITO_APP_CLIENT_SECRET']
    redirect_uri = current_app.config['COGNITO_REDIRECT_URI']
    
    # Basic認証ヘッダーを作成
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    token_response = requests.post(
        token_endpoint,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {auth_header}'
        },
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
    )
    
    if token_response.status_code != 200:
        return jsonify({'error': 'Failed to exchange token'}), 400
    
    tokens = token_response.json()
    
    # ユーザー情報を取得
    userinfo_endpoint = f"https://{current_app.config['COGNITO_DOMAIN']}/oauth2/userInfo"
    userinfo_response = requests.get(
        userinfo_endpoint,
        headers={'Authorization': f"Bearer {tokens['access_token']}"}
    )
    
    if userinfo_response.status_code != 200:
        return jsonify({'error': 'Failed to get user info'}), 400
    
    user_info = userinfo_response.json()
    
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
    
    return jsonify({
        'token': tokens['id_token'],
        'user': user.to_dict()
    })

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """ログアウトエンドポイント"""
    if not current_app.config['USE_COGNITO']:
        # 開発モード - 単純にOKを返す
        return jsonify({'message': 'Logged out successfully'})
    
    # 本番モード - CognitoログアウトURLを返す
    cognito_domain = current_app.config['COGNITO_DOMAIN']
    client_id = current_app.config['COGNITO_APP_CLIENT_ID']
    logout_uri = current_app.config['COGNITO_LOGOUT_URI']
    
    logout_url = f"https://{cognito_domain}/logout?" + urlencode({
        'client_id': client_id,
        'logout_uri': logout_uri
    })
    
    return jsonify({
        'logout_url': logout_url
    })