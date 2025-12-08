"""
Pytest configuration and fixtures for the BillGenerator backend.
"""
import pytest
import tempfile
import os
from backend.app import create_app
from backend.db import db
from backend.models.user import User
from backend.models.invoice import Invoice

@pytest.fixture
def app():
    """Create a Flask app instance for testing with an in-memory SQLite database."""
    # Create a temporary file for the SQLite database
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
    })
    
    with app.app_context():
        # Create all tables
        db.create_all()
        yield app
        
        # Clean up
        db.drop_all()
    
    # Close and remove the temporary database file
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    """Initialize the database with test data."""
    with app.app_context():
        # Create test users
        user1 = User(username='testuser1', email='test1@example.com')
        user1.set_password('password123')
        
        user2 = User(username='testuser2', email='test2@example.com')
        user2.set_password('password456')
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # Create test invoices
        invoice1 = Invoice(
            invoice_number='INV-001',
            client_name='Test Client 1',
            work_order_number='WO-001',
            bill_date='2023-01-15',
            due_date='2023-02-15',
            subtotal=1000.0,
            total_amount=1180.0,
            amount_paid=0.0,
            unpaid_amount=1180.0,
            user_id=user1.id
        )
        
        invoice2 = Invoice(
            invoice_number='INV-002',
            client_name='Test Client 2',
            work_order_number='WO-002',
            bill_date='2023-01-20',
            due_date='2023-02-20',
            subtotal=2000.0,
            total_amount=2360.0,
            amount_paid=500.0,
            unpaid_amount=1860.0,
            user_id=user2.id
        )
        
        db.session.add(invoice1)
        db.session.add(invoice2)
        db.session.commit()
        
        yield db

@pytest.fixture
def auth_header(client):
    """Get authentication header for protected endpoints."""
    # Register a test user
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    
    # Login to get access token
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    data = response.get_json()
    access_token = data.get('access_token')
    
    return {'Authorization': f'Bearer {access_token}'}