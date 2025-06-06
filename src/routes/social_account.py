# Placeholder for social account routes (not used in tests)
from flask import Blueprint

social_account_bp = Blueprint('social_account', __name__, url_prefix='/api/social-accounts')

__all__ = ['social_account_bp']
