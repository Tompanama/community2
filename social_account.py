from src.models.base import db, BaseModel
from datetime import datetime

class SocialAccount(db.Model, BaseModel):
    """Social account model for connected social media platforms"""
    __tablename__ = 'social_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # facebook, instagram, linkedin, twitter, tiktok, youtube
    account_name = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.String(100), nullable=True)
    access_token = db.Column(db.Text, nullable=True)
    refresh_token = db.Column(db.Text, nullable=True)
    token_expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='social_accounts')
    post_schedules = db.relationship('PostSchedule', back_populates='social_account')
    analytics = db.relationship('Analytics', back_populates='social_account')
    
    def __repr__(self):
        return f'<SocialAccount {self.platform} - {self.account_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'platform': self.platform,
            'account_name': self.account_name,
            'account_id': self.account_id,
            'token_expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def is_token_valid(self):
        if not self.token_expires_at:
            return False
        return self.token_expires_at > datetime.utcnow()

