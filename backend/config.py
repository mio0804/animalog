import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class Config:
    # Flask設定
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://animalog:animalog@db:5432/animalog')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AWS S3
    USE_S3 = os.getenv('USE_S3', 'false').lower() == 'true'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    
    # Cognito設定
    USE_COGNITO = os.getenv('USE_COGNITO', 'false').lower() == 'true'
    COGNITO_REGION = os.getenv('COGNITO_REGION', 'ap-northeast-1')
    COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
    COGNITO_APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')
    COGNITO_APP_CLIENT_SECRET = os.getenv('COGNITO_APP_CLIENT_SECRET')
    COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
    COGNITO_REDIRECT_URI = os.getenv('COGNITO_REDIRECT_URI', 'http://localhost:3000/callback')
    COGNITO_LOGOUT_URI = os.getenv('COGNITO_LOGOUT_URI', 'http://localhost:3000/login')
    
    # ファイルアップロード設定
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/workspace/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # 開発用モックユーザー設定
    MOCK_USER_ID = os.getenv('MOCK_USER_ID', 'test-user-123')
    MOCK_USER_EMAIL = os.getenv('MOCK_USER_EMAIL', 'test@example.com')
    MOCK_USER_NAME = os.getenv('MOCK_USER_NAME', 'テスト')
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']