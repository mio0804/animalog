from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.pets import pets_bp
from routes.diaries import diaries_bp
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
    
    # Serve uploaded files in development
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
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