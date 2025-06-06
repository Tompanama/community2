from flask import Blueprint, jsonify
from .auth import token_required
from src.models import User

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    return jsonify({'success': True, 'user': user.to_dict()}), 200

__all__ = ['user_bp', 'token_required']
