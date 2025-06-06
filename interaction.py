from src.models.base import db, BaseModel

class Interaction(db.Model, BaseModel):
    """Interaction model for comments, likes, shares, and messages"""
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    post_schedule_id = db.Column(db.Integer, db.ForeignKey('post_schedules.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # comment, like, share, message
    content = db.Column(db.Text, nullable=True)
    author_name = db.Column(db.String(100), nullable=True)
    author_id = db.Column(db.String(100), nullable=True)
    platform_interaction_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, responded, ignored
    
    # Relationships
    post_schedule = db.relationship('PostSchedule', back_populates='interactions')
    
    def __repr__(self):
        return f'<Interaction {self.id} - {self.type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_schedule_id': self.post_schedule_id,
            'type': self.type,
            'content': self.content,
            'author_name': self.author_name,
            'author_id': self.author_id,
            'platform_interaction_id': self.platform_interaction_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

