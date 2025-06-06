"""
Tests for API routes
"""

import pytest
import json
from src.models.user import User
from src.models.organization import Organization
from src.models.base import db

def test_index_route(client):
    """Test the index route"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Welcome to Community AI API'

def test_register_user(client, app):
    """Test user registration"""
    # Register a new user
    response = client.post('/api/auth/register', json={
        'email': 'new_user@example.com',
        'password': 'password123',
        'first_name': 'New',
        'last_name': 'User'
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'user' in data
    assert data['user']['email'] == 'new_user@example.com'
    
    # Check that the user was created in the database
    with app.app_context():
        user = User.query.filter_by(email='new_user@example.com').first()
        assert user is not None
        assert user.first_name == 'New'
        assert user.last_name == 'User'

def test_login_user(client, app):
    """Test user login"""
    # Create a user
    with app.app_context():
        user = User(
            email='login_test@example.com',
            password='password123',
            first_name='Login',
            last_name='Test',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
    
    # Login with the user
    response = client.post('/api/auth/login', json={
        'email': 'login_test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'token' in data
    assert data['user']['email'] == 'login_test@example.com'

def test_get_user_profile(client, auth_token):
    """Test getting user profile"""
    # Get the user profile
    response = client.get('/api/users/profile', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'

def test_create_organization(client, auth_token, app):
    """Test creating an organization"""
    # Create an organization
    response = client.post('/api/organizations', json={
        'name': 'Test Organization',
        'description': 'A test organization'
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'organization' in data
    assert data['organization']['name'] == 'Test Organization'
    
    # Check that the organization was created in the database
    with app.app_context():
        org = Organization.query.filter_by(name='Test Organization').first()
        assert org is not None
        assert org.description == 'A test organization'
        
        # Get the user ID from the token
        import jwt
        decoded = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']
        
        # Check that the user is the owner
        assert org.owner_id == user_id

def test_get_organizations(client, auth_token, app):
    """Test getting user's organizations"""
    # Create a user and organization in the database
    with app.app_context():
        # Get the user ID from the token
        import jwt
        decoded = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']
        
        # Create an organization
        org = Organization(
            name='User Organization',
            description='An organization for testing',
            owner_id=user_id
        )
        db.session.add(org)
        db.session.commit()
    
    # Get the user's organizations
    response = client.get('/api/organizations', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'organizations' in data
    assert len(data['organizations']) >= 1
    
    # Check that the created organization is in the list
    org_names = [org['name'] for org in data['organizations']]
    assert 'User Organization' in org_names

def test_unauthorized_access(client):
    """Test unauthorized access to protected routes"""
    # Try to access a protected route without a token
    response = client.get('/api/users/profile')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'message' in data
    assert 'token is missing' in data['message'].lower()
    
    # Try to access a protected route with an invalid token
    response = client.get('/api/users/profile', headers={
        'Authorization': 'Bearer invalid_token'
    })
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'message' in data
    assert 'invalid token' in data['message'].lower()

def test_ai_assistant_routes(client, auth_token, monkeypatch):
    """Test AI assistant routes with mocked AI services"""
    # Mock the TextGenerationService.generate_text method
    from src.services.ai.text_generation import TextGenerationService
    
    original_generate_text = TextGenerationService.generate_text
    
    def mock_generate_text(self, prompt, **kwargs):
        return {
            'success': True,
            'data': f"Generated text for prompt: {prompt}"
        }
    
    # Apply the mock
    monkeypatch.setattr(TextGenerationService, 'generate_text', mock_generate_text)
    
    # Test the generate-text endpoint
    response = client.post('/api/ai/generate-text', json={
        'prompt': 'Test prompt'
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'data' in data
    assert data['data'] == "Generated text for prompt: Test prompt"
    
    # Restore the original method
    monkeypatch.setattr(TextGenerationService, 'generate_text', original_generate_text)

def test_uploads_directory(client):
    """Test access to the uploads directory"""
    # Create a test file in the uploads directory
    import os
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    test_file_path = os.path.join(uploads_dir, 'test_file.txt')
    with open(test_file_path, 'w') as f:
        f.write('Test file content')
    
    # Try to access the file
    response = client.get('/uploads/test_file.txt')
    
    assert response.status_code == 200
    assert response.data == b'Test file content'
    
    # Clean up
    os.remove(test_file_path)

