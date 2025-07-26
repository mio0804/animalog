from flask import Blueprint, jsonify
from auth import get_current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/me', methods=['GET'])
def get_me():
    """現在のユーザー情報を取得"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({'user': user.to_dict()})

# ログインエンドポイントは削除（フロントエンドで直接Cognitoと通信）

# コールバックエンドポイントは削除（フロントエンドでAmplifyが処理）

# ログアウトエンドポイントは削除（フロントエンドでAmplifyが処理）