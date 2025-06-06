from src.models.base import db, BaseModel
import json

class AutoResponse(db.Model, BaseModel):
    """Auto response model for automated interaction responses"""
    __tablename__ = 'auto_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    trigger_type = db.Column(db.String(50), nullable=False)  # keyword, sentiment, question
    trigger_value = db.Column(db.Text, nullable=False)
    response_template = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='auto_responses')
    
    def __repr__(self):
        return f'<AutoResponse {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'name': self.name,
            'trigger_type': self.trigger_type,
            'trigger_value': self.trigger_value,
            'response_template': self.response_template,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AIPrompt(db.Model, BaseModel):
    """AI prompt model for storing custom AI prompts"""
    __tablename__ = 'ai_prompts'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    prompt_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # text, image, video
    _parameters = db.Column('parameters', db.Text, nullable=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='ai_prompts')
    
    def __repr__(self):
        return f'<AIPrompt {self.name}>'
    
    @property
    def parameters(self):
        if self._parameters:
            return json.loads(self._parameters)
        return {}
    
    @parameters.setter
    def parameters(self, value):
        self._parameters = json.dumps(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'name': self.name,
            'description': self.description,
            'prompt_text': self.prompt_text,
            'category': self.category,
            'parameters': self.parameters,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

