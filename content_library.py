from src.models.base import db, BaseModel
import json

class ContentLibrary(db.Model, BaseModel):
    """Content library model for organizing media assets"""
    __tablename__ = 'content_libraries'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='content_libraries')
    media_assets = db.relationship('MediaAsset', back_populates='library')
    
    def __repr__(self):
        return f'<ContentLibrary {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MediaAsset(db.Model, BaseModel):
    """Media asset model for storing images, videos, and other media"""
    __tablename__ = 'media_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('content_libraries.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # image, video, audio
    url = db.Column(db.String(255), nullable=False)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    _metadata = db.Column('metadata', db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    
    # Relationships
    library = db.relationship('ContentLibrary', back_populates='media_assets')
    
    def __repr__(self):
        return f'<MediaAsset {self.id} - {self.type}>'
    
    @property
    def metadata(self):
        if self._metadata:
            return json.loads(self._metadata)
        return {}
    
    @metadata.setter
    def metadata(self, value):
        self._metadata = json.dumps(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'library_id': self.library_id,
            'type': self.type,
            'url': self.url,
            'thumbnail_url': self.thumbnail_url,
            'metadata': self.metadata,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

