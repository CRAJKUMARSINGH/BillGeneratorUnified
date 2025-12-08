"""
Test cases for the authentication API endpoints.
"""
import pytest
import json
from backend.models.user import db, User

def test_register_user(client):
    """Test user registration."""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    
    response = client.post('/api/auth/register',
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'user' in data
    assert data['user']['username'] == 'testuser'
    assert data['user']['email'] == 'test@example.com'
    assert 'password' not in data['user']

def test_register_duplicate_user(client):
    """Test registering a duplicate user."""
    # Register first user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    
    client.post('/api/auth/register',
                data=json.dumps(user_data),
                content_type='application/json')
    
    # Try to register the same user again
    response = client.post('/api/auth/register',
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    # Should return 409 Conflict, not 400 Bad Request
    assert response.status_code == 409
    
    data = json.loads(response.data)
    assert 'error' in data

def test_login_user(client):
    """Test user login."""
    # First register a user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    
    client.post('/api/auth/register',
                data=json.dumps(user_data),
                content_type='application/json')
    
    # Then login
    login_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    
    response = client.post('/api/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'user' in data
    assert data['user']['username'] == 'testuser'

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    login_data = {
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    }
    
    response = client.post('/api/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 401
    
    data = json.loads(response.data)
    assert 'error' in data

def test_protected_route_without_token(client):
    """Test accessing a protected route without a token."""
    response = client.get('/api/auth/profile')
    assert response.status_code == 401

def test_protected_route_with_valid_token(client):
    """Test accessing a protected route with a valid token."""
    # Register and login to get a token
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    
    client.post('/api/auth/register',
                data=json.dumps(user_data),
                content_type='application/json')
    
    login_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    
    response = client.post('/api/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    data = json.loads(response.data)
    access_token = data['access_token']
    
    # Access protected route with token
    response = client.get('/api/auth/profile',
                         headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 200