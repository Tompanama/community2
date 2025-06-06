"""
Configuration for pytest
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

from src.main import app as flask_app
from src.models.base import db

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Set up the test configuration
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key'
    })

    # Create the database and tables
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app"""
    return app.test_cli_runner()

@pytest.fixture
def auth_token(client):
    """Get an authentication token for testing"""
    # Create a test user
    from src.models.user import User
    import jwt
    import datetime
    
    with flask_app.app_context():
        # Check if test user exists
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            # Create test user
            user = User(
                email='test@example.com',
                password='password123',
                first_name='Test',
                last_name='User',
                is_active=True
            )
            db.session.add(user)
            db.session.commit()
        
        # Generate token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, flask_app.config['SECRET_KEY'], algorithm='HS256')
        
        return token

