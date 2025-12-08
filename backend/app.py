"""
Flask Backend for BillGenerator Unified
Implements security improvements as per the security review
"""
from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import os

# Import Flask extensions
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Import the shared database instance
from backend.db import db

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configure logging
    if not app.debug and not app.testing:
        # Set up file logging with rotation
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/billgenerator.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('BillGenerator startup')
    
    # Configuration from environment variables
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key-for-dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///billgenerator.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with the app
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Initialize CORS
    CORS(app, origins=os.environ.get('CORS_ORIGINS', '*').split(','))
    
    # Initialize Rate Limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[os.environ.get('RATE_LIMIT_DEFAULT', '1000 per hour')],
        storage_uri=os.environ.get('RATE_LIMIT_STORAGE', 'memory://'),
        app=app
    )
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        app.logger.info('Health check endpoint accessed')
        return jsonify({"status": "healthy", "message": "BillGenerator backend is running"})
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='BillGenerator API',
        description='API for the BillGenerator Unified application',
        doc='/docs/',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
            }
        },
        security='Bearer'
    )
    
    # Define API namespaces
    ns_auth = api.namespace('auth', description='Authentication operations')
    ns_invoices = api.namespace('invoices', description='Invoice operations')
    ns_users = api.namespace('users', description='User operations')
    
    # Define API models
    user_input_model = api.model('UserInput', {
        'username': fields.String(required=True, description='Username'),
        'email': fields.String(required=True, description='Email address'),
        'password': fields.String(required=True, description='Password')
    })
    
    user_login_model = api.model('UserLogin', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    })
    
    user_model = api.model('User', {
        'id': fields.Integer(readonly=True, description='User identifier'),
        'username': fields.String(required=True, description='Username'),
        'email': fields.String(required=True, description='Email address'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'is_active': fields.Boolean(default=True, description='User activation status')
    })
    
    user_response_model = api.model('UserResponse', {
        'user': fields.Nested(user_model, description='User information')
    })
    
    user_list_model = api.model('UserList', {
        'users': fields.List(fields.Nested(user_model)),
        'pagination': fields.Raw(description='Pagination metadata')
    })
    
    invoice_input_model = api.model('InvoiceInput', {
        'invoice_number': fields.String(required=True, description='Invoice number'),
        'client_name': fields.String(required=True, description='Client name'),
        'work_order_number': fields.String(required=True, description='Work order number'),
        'bill_date': fields.Date(required=True, description='Bill date (YYYY-MM-DD)'),
        'due_date': fields.Date(required=True, description='Due date (YYYY-MM-DD)'),
        'subtotal': fields.Float(required=True, description='Subtotal amount'),
        'total_amount': fields.Float(required=True, description='Total amount'),
        'amount_paid': fields.Float(default=0.0, description='Amount paid'),
        'unpaid_amount': fields.Float(default=0.0, description='Unpaid amount')
    })
    
    invoice_model = api.model('Invoice', {
        'id': fields.Integer(readonly=True, description='Invoice identifier'),
        'invoice_number': fields.String(required=True, description='Invoice number'),
        'client_name': fields.String(required=True, description='Client name'),
        'work_order_number': fields.String(required=True, description='Work order number'),
        'bill_date': fields.Date(required=True, description='Bill date'),
        'due_date': fields.Date(required=True, description='Due date'),
        'subtotal': fields.Float(required=True, description='Subtotal amount'),
        'total_amount': fields.Float(required=True, description='Total amount'),
        'amount_paid': fields.Float(default=0.0, description='Amount paid'),
        'unpaid_amount': fields.Float(default=0.0, description='Unpaid amount'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'user_id': fields.Integer(required=True, description='User identifier')
    })
    
    invoice_response_model = api.model('InvoiceResponse', {
        'invoice': fields.Nested(invoice_model, description='Invoice information')
    })
    
    invoice_list_model = api.model('InvoiceList', {
        'invoices': fields.List(fields.Nested(invoice_model)),
        'pagination': fields.Raw(description='Pagination metadata')
    })
    
    token_model = api.model('Token', {
        'access_token': fields.String(description='JWT access token'),
        'message': fields.String(description='Response message')
    })
    
    error_model = api.model('Error', {
        'error': fields.String(description='Error message')
    })
    
    message_model = api.model('Message', {
        'message': fields.String(description='Response message')
    })
    
    # Register blueprints
    from backend.routes import auth, invoices, products, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(invoices.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(users.bp)
    
    # Add RESTX resources for documentation
    @ns_auth.route('/register')
    class AuthRegister(Resource):
        @api.doc('register_user')
        @api.expect(user_input_model)
        @api.marshal_with(token_model, code=201)
        @api.response(400, 'Validation Error', error_model)
        @api.response(409, 'User Already Exists', error_model)
        @api.response(500, 'Registration Failed', error_model)
        @limiter.limit("5 per minute")  # Rate limit for registration
        def post(self):
            """Register a new user"""
            pass  # Actual implementation is in the blueprint
    
    @ns_auth.route('/login')
    class AuthLogin(Resource):
        @api.doc('login_user')
        @api.expect(user_login_model)
        @api.marshal_with(token_model, code=200)
        @api.response(400, 'Validation Error', error_model)
        @api.response(401, 'Invalid Credentials', error_model)
        @api.response(500, 'Login Failed', error_model)
        @limiter.limit("10 per minute")  # Rate limit for login attempts
        def post(self):
            """Login user"""
            pass  # Actual implementation is in the blueprint
    
    @ns_auth.route('/profile')
    class AuthProfile(Resource):
        @api.doc('get_user_profile')
        @api.marshal_with(user_response_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(404, 'User Not Found', error_model)
        @api.response(500, 'Profile Retrieval Failed', error_model)
        def get(self):
            """Get user profile"""
            pass  # Actual implementation is in the blueprint
    
    @ns_users.route('')
    class UsersList(Resource):
        @api.doc('get_users')
        @api.marshal_with(user_list_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(500, 'Users Retrieval Failed', error_model)
        def get(self):
            """Get all users with pagination"""
            pass  # Actual implementation is in the blueprint
    
    @ns_users.route('/<int:user_id>')
    @api.param('user_id', 'User identifier')
    class Users(Resource):
        @api.doc('get_user')
        @api.marshal_with(user_response_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(404, 'User Not Found', error_model)
        @api.response(500, 'User Retrieval Failed', error_model)
        def get(self, user_id):
            """Get a specific user"""
            pass  # Actual implementation is in the blueprint
        
        @api.doc('update_user')
        @api.expect(user_model)
        @api.marshal_with(user_response_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(404, 'User Not Found', error_model)
        @api.response(500, 'User Update Failed', error_model)
        def put(self, user_id):
            """Update an existing user"""
            pass  # Actual implementation is in the blueprint
        
        @api.doc('delete_user')
        @api.marshal_with(message_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(404, 'User Not Found', error_model)
        @api.response(500, 'User Deletion Failed', error_model)
        def delete(self, user_id):
            """Delete a user"""
            pass  # Actual implementation is in the blueprint
    
    @ns_invoices.route('')
    class InvoicesList(Resource):
        @api.doc('get_invoices')
        @api.marshal_with(invoice_list_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(500, 'Invoices Retrieval Failed', error_model)
        def get(self):
            """Get all invoices with pagination"""
            pass  # Actual implementation is in the blueprint
        
        @api.doc('create_invoice')
        @api.expect(invoice_input_model)
        @api.marshal_with(invoice_response_model, code=201)
        @api.response(400, 'Validation Error', error_model)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(500, 'Invoice Creation Failed', error_model)
        def post(self):
            """Create a new invoice"""
            pass  # Actual implementation is in the blueprint
    
    @ns_invoices.route('/<int:invoice_id>')
    @api.param('invoice_id', 'Invoice identifier')
    class Invoices(Resource):
        @api.doc('get_invoice')
        @api.marshal_with(invoice_response_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(404, 'Invoice Not Found', error_model)
        @api.response(500, 'Invoice Retrieval Failed', error_model)
        def get(self, invoice_id):
            """Get a specific invoice"""
            pass  # Actual implementation is in the blueprint
        
        @api.doc('update_invoice')
        @api.expect(invoice_model)
        @api.marshal_with(invoice_response_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(404, 'Invoice Not Found', error_model)
        @api.response(500, 'Invoice Update Failed', error_model)
        def put(self, invoice_id):
            """Update an existing invoice"""
            pass  # Actual implementation is in the blueprint
        
        @api.doc('delete_invoice')
        @api.marshal_with(message_model, code=200)
        @api.response(401, 'Unauthorized', error_model)
        @api.response(404, 'Invoice Not Found', error_model)
        @api.response(500, 'Invoice Deletion Failed', error_model)
        def delete(self, invoice_id):
            """Delete an invoice"""
            pass  # Actual implementation is in the blueprint
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')