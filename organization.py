from src.models.base import db, BaseModel

class Organization(db.Model, BaseModel):
    """Organization model for grouping users and social accounts"""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='owned_organizations')
    
    # Relationships
    members = db.relationship('OrganizationMember', back_populates='organization')
    social_accounts = db.relationship('SocialAccount', back_populates='organization')
    content_libraries = db.relationship('ContentLibrary', back_populates='organization')
    content_templates = db.relationship('ContentTemplate', back_populates='organization')
    posts = db.relationship('Post', back_populates='organization')
    auto_responses = db.relationship('AutoResponse', back_populates='organization')
    ai_prompts = db.relationship('AIPrompt', back_populates='organization')
    
    def __repr__(self):
        return f'<Organization {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo': self.logo,
            'industry': self.industry,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class OrganizationMember(db.Model, BaseModel):
    """Organization member model for user-organization relationships"""
    __tablename__ = 'organization_members'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='member')  # owner, admin, editor, viewer
    
    # Relationships
    organization = db.relationship('Organization', back_populates='members')
    user = db.relationship('User', back_populates='organizations')
    
    __table_args__ = (
        db.UniqueConstraint('organization_id', 'user_id', name='unique_org_user'),
    )
    
    def __repr__(self):
        return f'<OrganizationMember {self.user_id} in {self.organization_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'user_id': self.user_id,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

