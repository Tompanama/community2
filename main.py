import os
import sys
# DON'T CHANGE THIS LINE
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from src.models.base import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.organization import organization_bp
from src.routes.social_account import social_account_bp
from src.routes.post import post_bp
from src.routes.ai_assistant import ai_assistant_bp
from src.models import User, Organization, OrganizationMember, SocialAccount, ContentLibrary, MediaAsset, ContentTemplate, Post, PostSchedule, Interaction, AutoResponse, AIPrompt, Analytics, Report
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create uploads directory if it doesn't exist
uploads_dir = os.path.join(os.getcwd(), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(os.path.join(uploads_dir, 'images'), exist_ok=True)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///community_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(organization_bp)
app.register_blueprint(social_account_bp)
app.register_blueprint(post_bp)
app.register_blueprint(ai_assistant_bp)

# Serve uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(uploads_dir, filename)

# Root route
@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to Community AI API',
        'version': '1.0.0'
    })

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

