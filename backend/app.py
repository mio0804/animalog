from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.pets import pets_bp
from routes.diaries import diaries_bp
from routes.images import images_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(diaries_bp)
    app.register_blueprint(images_bp)
    
    # Serve uploaded files in development
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        if app.config['USE_S3']:
            # Redirect to S3 URL when USE_S3 is true
            s3_url = f"https://{app.config['S3_BUCKET_NAME']}.s3.{app.config['AWS_REGION']}.amazonaws.com/diary-images/{filename}"
            from flask import redirect
            return redirect(s3_url)
        else:
            # Serve from local folder when USE_S3 is false
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)