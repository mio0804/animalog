from flask import Blueprint, jsonify, request, current_app
from auth import get_current_user

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
                'email': current_app.config['MOCK_USER_EMAIL']
            }
        })
    
    # 本番モード - Cognitoトークンを検証
    data = request.get_json()
    token = data.get('token')
    
    if not token:
        return jsonify({'error': 'Token required'}), 400
    
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Invalid token'}), 401
    
    return jsonify({
        'user': user.to_dict()
    })