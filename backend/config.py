import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://animalog:animalog@db:5432/animalog')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AWS S3
    USE_S3 = os.getenv('USE_S3', 'false').lower() == 'true'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    
    # Cognito
    USE_COGNITO = os.getenv('USE_COGNITO', 'false').lower() == 'true'
    COGNITO_REGION = os.getenv('COGNITO_REGION', 'ap-northeast-1')
    COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
    COGNITO_APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')
    
    # File Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/workspace/uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Mock User for Development
    MOCK_USER_ID = os.getenv('MOCK_USER_ID', 'test-user-123')
    MOCK_USER_EMAIL = os.getenv('MOCK_USER_EMAIL', 'test@example.com')
    MOCK_USER_NAME = os.getenv('MOCK_USER_NAME', 'テスト')
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']