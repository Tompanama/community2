from src.models.base import db, BaseModel
import json

class Analytics(db.Model, BaseModel):
    """Analytics model for storing metrics and performance data"""
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    social_account_id = db.Column(db.Integer, db.ForeignKey('social_accounts.id'), nullable=False)
    post_schedule_id = db.Column(db.Integer, db.ForeignKey('post_schedules.id'), nullable=True)
    metric_type = db.Column(db.String(50), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    # Relationships
    organization = db.relationship('Organization')
    social_account = db.relationship('SocialAccount', back_populates='analytics')
    
    def __repr__(self):
        return f'<Analytics {self.id} - {self.metric_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'social_account_id': self.social_account_id,
            'post_schedule_id': self.post_schedule_id,
            'metric_type': self.metric_type,
            'metric_value': self.metric_value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Report(db.Model, BaseModel):
    """Report model for storing report configurations"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # weekly, monthly, custom
    _parameters = db.Column('parameters', db.Text, nullable=False)
    last_generated = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    organization = db.relationship('Organization')
    
    def __repr__(self):
        return f'<Report {self.name}>'
    
    @property
    def parameters(self):
        return json.loads(self._parameters)
    
    @parameters.setter
    def parameters(self, value):
        self._parameters = json.dumps(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'name': self.name,
            'type': self.type,
            'parameters': self.parameters,
            'last_generated': self.last_generated.isoformat() if self.last_generated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

