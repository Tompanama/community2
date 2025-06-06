"""
Tests for database models
"""

import pytest
from src.models.user import User
from src.models.organization import Organization, OrganizationMember
from src.models.social_account import SocialAccount
from src.models.content import ContentTemplate, Post, PostSchedule
from src.models.base import db

def test_user_model(app):
    """Test the User model"""
    with app.app_context():
        # Create a user
        user = User(
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Query the user
        queried_user = User.query.filter_by(email='test@example.com').first()
        
        # Check that the user was created correctly
        assert queried_user is not None
        assert queried_user.email == 'test@example.com'
        assert queried_user.first_name == 'Test'
        assert queried_user.last_name == 'User'
        assert queried_user.is_active == True
        assert queried_user.check_password('password123') == True
        assert queried_user.check_password('wrong_password') == False

def test_organization_model(app):
    """Test the Organization model"""
    with app.app_context():
        # Create a user
        user = User(
            email='org_owner@example.com',
            password='password123',
            first_name='Org',
            last_name='Owner',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Create an organization
        org = Organization(
            name='Test Organization',
            description='A test organization',
            owner_id=user.id
        )
        db.session.add(org)
        db.session.commit()
        
        # Query the organization
        queried_org = Organization.query.filter_by(name='Test Organization').first()
        
        # Check that the organization was created correctly
        assert queried_org is not None
        assert queried_org.name == 'Test Organization'
        assert queried_org.description == 'A test organization'
        assert queried_org.owner_id == user.id
        
        # Check the relationship with the owner
        assert queried_org.owner.email == 'org_owner@example.com'

def test_organization_member_model(app):
    """Test the OrganizationMember model"""
    with app.app_context():
        # Create users
        owner = User(
            email='org_owner@example.com',
            password='password123',
            first_name='Org',
            last_name='Owner',
            is_active=True
        )
        member = User(
            email='org_member@example.com',
            password='password123',
            first_name='Org',
            last_name='Member',
            is_active=True
        )
        db.session.add_all([owner, member])
        db.session.commit()
        
        # Create an organization
        org = Organization(
            name='Test Organization',
            description='A test organization',
            owner_id=owner.id
        )
        db.session.add(org)
        db.session.commit()
        
        # Add a member to the organization
        org_member = OrganizationMember(
            organization_id=org.id,
            user_id=member.id,
            role='editor'
        )
        db.session.add(org_member)
        db.session.commit()
        
        # Query the organization member
        queried_member = OrganizationMember.query.filter_by(
            organization_id=org.id,
            user_id=member.id
        ).first()
        
        # Check that the organization member was created correctly
        assert queried_member is not None
        assert queried_member.organization_id == org.id
        assert queried_member.user_id == member.id
        assert queried_member.role == 'editor'
        
        # Check the relationships
        assert queried_member.organization.name == 'Test Organization'
        assert queried_member.user.email == 'org_member@example.com'

def test_social_account_model(app):
    """Test the SocialAccount model"""
    with app.app_context():
        # Create a user
        user = User(
            email='social_user@example.com',
            password='password123',
            first_name='Social',
            last_name='User',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Create an organization
        org = Organization(
            name='Social Organization',
            description='An organization with social accounts',
            owner_id=user.id
        )
        db.session.add(org)
        db.session.commit()
        
        # Create a social account
        social_account = SocialAccount(
            organization_id=org.id,
            platform='instagram',
            username='test_instagram',
            access_token='test_token',
            refresh_token='refresh_token',
            token_expires_at='2025-12-31 23:59:59',
            is_active=True
        )
        db.session.add(social_account)
        db.session.commit()
        
        # Query the social account
        queried_account = SocialAccount.query.filter_by(
            organization_id=org.id,
            platform='instagram'
        ).first()
        
        # Check that the social account was created correctly
        assert queried_account is not None
        assert queried_account.organization_id == org.id
        assert queried_account.platform == 'instagram'
        assert queried_account.username == 'test_instagram'
        assert queried_account.access_token == 'test_token'
        assert queried_account.is_active == True
        
        # Check the relationship with the organization
        assert queried_account.organization.name == 'Social Organization'

def test_content_template_model(app):
    """Test the ContentTemplate model"""
    with app.app_context():
        # Create a user
        user = User(
            email='template_user@example.com',
            password='password123',
            first_name='Template',
            last_name='User',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Create an organization
        org = Organization(
            name='Template Organization',
            description='An organization with content templates',
            owner_id=user.id
        )
        db.session.add(org)
        db.session.commit()
        
        # Create a content template
        template = ContentTemplate(
            organization_id=org.id,
            name='Product Launch Template',
            content='Découvrez notre nouveau produit: {product_name}! {product_description} #nouveauté #{product_category} #innovation',
            template_type='text',
            platform='instagram',
            created_by=user.id
        )
        db.session.add(template)
        db.session.commit()
        
        # Query the content template
        queried_template = ContentTemplate.query.filter_by(
            organization_id=org.id,
            name='Product Launch Template'
        ).first()
        
        # Check that the content template was created correctly
        assert queried_template is not None
        assert queried_template.organization_id == org.id
        assert queried_template.name == 'Product Launch Template'
        assert queried_template.template_type == 'text'
        assert queried_template.platform == 'instagram'
        assert queried_template.created_by == user.id
        
        # Check the relationships
        assert queried_template.organization.name == 'Template Organization'
        assert queried_template.creator.email == 'template_user@example.com'

def test_post_model(app):
    """Test the Post model"""
    with app.app_context():
        # Create a user
        user = User(
            email='post_user@example.com',
            password='password123',
            first_name='Post',
            last_name='User',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Create an organization
        org = Organization(
            name='Post Organization',
            description='An organization with posts',
            owner_id=user.id
        )
        db.session.add(org)
        db.session.commit()
        
        # Create a social account
        social_account = SocialAccount(
            organization_id=org.id,
            platform='facebook',
            username='test_facebook',
            access_token='test_token',
            refresh_token='refresh_token',
            token_expires_at='2025-12-31 23:59:59',
            is_active=True
        )
        db.session.add(social_account)
        db.session.commit()
        
        # Create a post
        post = Post(
            organization_id=org.id,
            social_account_id=social_account.id,
            content='This is a test post',
            media_urls='["http://example.com/image.jpg"]',
            post_type='image',
            status='draft',
            created_by=user.id
        )
        db.session.add(post)
        db.session.commit()
        
        # Query the post
        queried_post = Post.query.filter_by(
            organization_id=org.id,
            content='This is a test post'
        ).first()
        
        # Check that the post was created correctly
        assert queried_post is not None
        assert queried_post.organization_id == org.id
        assert queried_post.social_account_id == social_account.id
        assert queried_post.content == 'This is a test post'
        assert queried_post.post_type == 'image'
        assert queried_post.status == 'draft'
        assert queried_post.created_by == user.id
        
        # Check the relationships
        assert queried_post.organization.name == 'Post Organization'
        assert queried_post.social_account.platform == 'facebook'
        assert queried_post.creator.email == 'post_user@example.com'

def test_post_schedule_model(app):
    """Test the PostSchedule model"""
    with app.app_context():
        # Create a user
        user = User(
            email='schedule_user@example.com',
            password='password123',
            first_name='Schedule',
            last_name='User',
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Create an organization
        org = Organization(
            name='Schedule Organization',
            description='An organization with scheduled posts',
            owner_id=user.id
        )
        db.session.add(org)
        db.session.commit()
        
        # Create a social account
        social_account = SocialAccount(
            organization_id=org.id,
            platform='twitter',
            username='test_twitter',
            access_token='test_token',
            refresh_token='refresh_token',
            token_expires_at='2025-12-31 23:59:59',
            is_active=True
        )
        db.session.add(social_account)
        db.session.commit()
        
        # Create a post
        post = Post(
            organization_id=org.id,
            social_account_id=social_account.id,
            content='This is a scheduled post',
            post_type='text',
            status='scheduled',
            created_by=user.id
        )
        db.session.add(post)
        db.session.commit()
        
        # Create a post schedule
        schedule = PostSchedule(
            post_id=post.id,
            scheduled_time='2025-06-15 12:00:00',
            timezone='Europe/Paris',
            status='pending'
        )
        db.session.add(schedule)
        db.session.commit()
        
        # Query the post schedule
        queried_schedule = PostSchedule.query.filter_by(post_id=post.id).first()
        
        # Check that the post schedule was created correctly
        assert queried_schedule is not None
        assert queried_schedule.post_id == post.id
        assert queried_schedule.scheduled_time == '2025-06-15 12:00:00'
        assert queried_schedule.timezone == 'Europe/Paris'
        assert queried_schedule.status == 'pending'
        
        # Check the relationship with the post
        assert queried_schedule.post.content == 'This is a scheduled post'

