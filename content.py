from src.models.base import db, BaseModel
import json

class ContentTemplate(db.Model, BaseModel):
    """Content template model for reusable content structures"""
    __tablename__ = 'content_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    _content = db.Column('content', db.Text, nullable=False)
    _platform_specific_settings = db.Column('platform_specific_settings', db.Text, nullable=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='content_templates')
    
    def __repr__(self):
        return f'<ContentTemplate {self.name}>'
    
    @property
    def content(self):
        return json.loads(self._content)
    
    @content.setter
    def content(self, value):
        self._content = json.dumps(value)
    
    @property
    def platform_specific_settings(self):
        if self._platform_specific_settings:
            return json.loads(self._platform_specific_settings)
        return {}
    
    @platform_specific_settings.setter
    def platform_specific_settings(self, value):
        self._platform_specific_settings = json.dumps(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'name': self.name,
            'description': self.description,
            'content': self.content,
            'platform_specific_settings': self.platform_specific_settings,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Post(db.Model, BaseModel):
    """Post model for social media content"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # text, image, video, carousel
    _content = db.Column('content', db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='draft')  # draft, scheduled, published, failed
    
    # Relationships
    organization = db.relationship('Organization', back_populates='posts')
    creator = db.relationship('User')
    schedules = db.relationship('PostSchedule', back_populates='post')
    
    def __repr__(self):
        return f'<Post {self.id} - {self.content_type}>'
    
    @property
    def content(self):
        return json.loads(self._content)
    
    @content.setter
    def content(self, value):
        self._content = json.dumps(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'creator_id': self.creator_id,
            'content_type': self.content_type,
            'content': self.content,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PostSchedule(db.Model, BaseModel):
    """Post schedule model for planning when posts are published"""
    __tablename__ = 'post_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    social_account_id = db.Column(db.Integer, db.ForeignKey('social_accounts.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    published_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, published, failed
    platform_post_id = db.Column(db.String(100), nullable=True)
    
    # Relationships
    post = db.relationship('Post', back_populates='schedules')
    social_account = db.relationship('SocialAccount', back_populates='post_schedules')
    interactions = db.relationship('Interaction', back_populates='post_schedule')
    
    def __repr__(self):
        return f'<PostSchedule {self.id} for post {self.post_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'social_account_id': self.social_account_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'published_time': self.published_time.isoformat() if self.published_time else None,
            'status': self.status,
            'platform_post_id': self.platform_post_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

