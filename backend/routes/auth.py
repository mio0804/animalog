from flask import Blueprint, jsonify, request, current_app
from auth import get_current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/me', methods=['GET'])
def get_me():
    """Get current user information"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({'user': user.to_dict()})

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint - in development mode, returns mock token"""
    if not current_app.config['USE_COGNITO']:
        # Development mode - return mock token
        return jsonify({
            'token': 'mock-development-token',
            'user': {
                'id': current_app.config['MOCK_USER_ID'],
                'email': current_app.config['MOCK_USER_EMAIL']
            }
        })
    
    # Production mode - validate Cognito token
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