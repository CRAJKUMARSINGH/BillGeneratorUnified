"""
Flask Backend for BillGenerator Unified
Implements security improvements as per the security review
"""
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration from environment variables
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key-for-dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///billgenerator.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db = SQLAlchemy(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    from backend.routes import auth, invoices, products, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(invoices.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(users.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "message": "BillGenerator backend is running"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')