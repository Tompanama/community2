from flask import Blueprint, jsonify, request
from src.models import db, Post, PostSchedule, SocialAccount
from src.routes.user import token_required
from src.routes.organization import is_org_member
from datetime import datetime

post_bp = Blueprint('post', __name__)

@post_bp.route('/organizations/<int:org_id>/posts', methods=['GET'])
@token_required
def get_posts(current_user_id, org_id):
    # Check if user is a member of the organization
    if not is_org_member(current_user_id, org_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Get query parameters for filtering
    status = request.args.get('status')
    content_type = request.args.get('content_type')
    creator_id = request.args.get('creator_id')
    
    # Build query
    query = Post.query.filter_by(organization_id=org_id)
    
    if status:
        query = query.filter_by(status=status)
    if content_type:
        query = query.filter_by(content_type=content_type)
    if creator_id:
        query = query.filter_by(creator_id=creator_id)
    
    # Sort by creation date, newest first
    posts = query.order_by(Post.created_at.desc()).all()
    
    return jsonify([post.to_dict() for post in posts])


@post_bp.route('/organizations/<int:org_id>/posts', methods=['POST'])
@token_required
def create_post(current_user_id, org_id):
    # Check if user is a member of the organization with at least editor role
    if not is_org_member(current_user_id, org_id, 'owner') and \
       not is_org_member(current_user_id, org_id, 'admin') and \
       not is_org_member(current_user_id, org_id, 'editor'):
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.json
    
    # Validate required fields
    if not all(k in data for k in ['content_type', 'content']):
        return jsonify({'message': 'Content type and content are required'}), 400
    
    # Validate content type
    valid_content_types = ['text', 'image', 'video', 'carousel']
    if data['content_type'] not in valid_content_types:
        return jsonify({'message': f'Content type must be one of: {", ".join(valid_content_types)}'}), 400
    
    # Create new post
    new_post = Post(
        organization_id=org_id,
        creator_id=current_user_id,
        content_type=data['content_type'],
        content=data['content'],
        status=data.get('status', 'draft')
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify(new_post.to_dict()), 201


@post_bp.route('/organizations/<int:org_id>/posts/<int:post_id>', methods=['GET'])
@token_required
def get_post(current_user_id, org_id, post_id):
    # Check if user is a member of the organization
    if not is_org_member(current_user_id, org_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    post = Post.query.filter_by(id=post_id, organization_id=org_id).first_or_404()
    return jsonify(post.to_dict())


@post_bp.route('/organizations/<int:org_id>/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user_id, org_id, post_id):
    # Check if user is a member of the organization with at least editor role
    if not is_org_member(current_user_id, org_id, 'owner') and \
       not is_org_member(current_user_id, org_id, 'admin') and \
       not is_org_member(current_user_id, org_id, 'editor'):
        return jsonify({'message': 'Unauthorized'}), 403
    
    post = Post.query.filter_by(id=post_id, organization_id=org_id).first_or_404()
    data = request.json
    
    # Update fields
    if 'content' in data:
        post.content = data['content']
    if 'content_type' in data:
        valid_content_types = ['text', 'image', 'video', 'carousel']
        if data['content_type'] not in valid_content_types:
            return jsonify({'message': f'Content type must be one of: {", ".join(valid_content_types)}'}), 400
        post.content_type = data['content_type']
    if 'status' in data:
        valid_statuses = ['draft', 'scheduled', 'published', 'failed']
        if data['status'] not in valid_statuses:
            return jsonify({'message': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
        post.status = data['status']
    
    db.session.commit()
    return jsonify(post.to_dict())


@post_bp.route('/organizations/<int:org_id>/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user_id, org_id, post_id):
    # Check if user is a member of the organization with at least editor role
    if not is_org_member(current_user_id, org_id, 'owner') and \
       not is_org_member(current_user_id, org_id, 'admin') and \
       not is_org_member(current_user_id, org_id, 'editor'):
        return jsonify({'message': 'Unauthorized'}), 403
    
    post = Post.query.filter_by(id=post_id, organization_id=org_id).first_or_404()
    
    # Delete all schedules for this post
    PostSchedule.query.filter_by(post_id=post_id).delete()
    
    # Delete post
    db.session.delete(post)
    db.session.commit()
    
    return '', 204


@post_bp.route('/organizations/<int:org_id>/posts/<int:post_id>/schedules', methods=['GET'])
@token_required
def get_post_schedules(current_user_id, org_id, post_id):
    # Check if user is a member of the organization
    if not is_org_member(current_user_id, org_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Verify post exists and belongs to organization
    post = Post.query.filter_by(id=post_id, organization_id=org_id).first_or_404()
    
    schedules = PostSchedule.query.filter_by(post_id=post_id).all()
    return jsonify([schedule.to_dict() for schedule in schedules])


@post_bp.route('/organizations/<int:org_id>/posts/<int:post_id>/schedules', methods=['POST'])
@token_required
def create_post_schedule(current_user_id, org_id, post_id):
    # Check if user is a member of the organization with at least editor role
    if not is_org_member(current_user_id, org_id, 'owner') and \
       not is_org_member(current_user_id, org_id, 'admin') and \
       not is_org_member(current_user_id, org_id, 'editor'):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Verify post exists and belongs to organization
    post = Post.query.filter_by(id=post_id, organization_id=org_id).first_or_404()
    
    data = request.json
    
    # Validate required fields
    if not all(k in data for k in ['social_account_id', 'scheduled_time']):
        return jsonify({'message': 'Social account ID and scheduled time are required'}), 400
    
    # Verify social account exists and belongs to organization
    social_account = SocialAccount.query.filter_by(
        id=data['social_account_id'],
        organization_id=org_id
    ).first_or_404()
    
    # Parse scheduled time
    try:
        scheduled_time = datetime.fromisoformat(data['scheduled_time'])
    except ValueError:
        return jsonify({'message': 'Invalid scheduled time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    # Create new schedule
    new_schedule = PostSchedule(
        post_id=post_id,
        social_account_id=data['social_account_id'],
        scheduled_time=scheduled_time,
        status='pending'
    )
    
    db.session.add(new_schedule)
    
    # Update post status to scheduled if it was a draft
    if post.status == 'draft':
        post.status = 'scheduled'
    
    db.session.commit()
    
    return jsonify(new_schedule.to_dict()), 201


@post_bp.route('/organizations/<int:org_id>/posts/<int:post_id>/schedules/<int:schedule_id>', methods=['PUT'])
@token_required
def update_post_schedule(current_user_id, org_id, post_id, schedule_id):
    # Check if user is a member of the organization with at least editor role
    if not is_org_member(current_user_id, org_id, 'owner') and \
       not is_org_member(current_user_id, org_id, 'admin') and \
       not is_org_member(current_user_id, org_id, 'editor'):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Verify post exists and belongs to organization
    post = Post.query.filter_by(id=post_id, organization_id=org_id).first_or_404()
    
    # Verify schedule exists and belongs to post
    schedule = PostSchedule.query.filter_by(id=schedule_id, post_id=post_id).first_or_404()
    
    data = request.json
    
    # Update fields
    if 'scheduled_time' in data:
        try:
            scheduled_time = datetime.fromisoformat(data['scheduled_time'])
            schedule.scheduled_time = scheduled_time
        except ValueError:
            return jsonify({'message': 'Invalid scheduled time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    if 'status' in data:
        valid_statuses = ['pending', 'published', 'failed']
        if data['status'] not in valid_statuses:
            return jsonify({'message': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
        schedule.status = data['status']
        
        # If status is changed to published, update published_time
        if data['status'] == 'published':
            schedule.published_time = datetime.utcnow()
    
    if 'platform_post_id' in data:
        schedule.platform_post_id = data['platform_post_id']
    
    db.session.commit()
    return jsonify(schedule.to_dict())


@post_bp.route('/organizations/<int:org_id>/posts/<int:post_id>/schedules/<int:schedule_id>', methods=['DELETE'])
@token_required
def delete_post_schedule(current_user_id, org_id, post_id, schedule_id):
    # Check if user is a member of the organization with at least editor role
    if not is_org_member(current_user_id, org_id, 'owner') and \
       not is_org_member(current_user_id, org_id, 'admin') and \
       not is_org_member(current_user_id, org_id, 'editor'):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Verify post exists and belongs to organization
    post = Post.query.filter_by(id=post_id, organization_id=org_id).first_or_404()
    
    # Verify schedule exists and belongs to post
    schedule = PostSchedule.query.filter_by(id=schedule_id, post_id=post_id).first_or_404()
    
    db.session.delete(schedule)
    
    # If this was the only schedule and it's not published, set post back to draft
    remaining_schedules = PostSchedule.query.filter_by(post_id=post_id).count()
    if remaining_schedules == 0 and post.status == 'scheduled':
        post.status = 'draft'
    
    db.session.commit()
    
    return '', 204


@post_bp.route('/organizations/<int:org_id>/calendar', methods=['GET'])
@token_required
def get_calendar(current_user_id, org_id):
    # Check if user is a member of the organization
    if not is_org_member(current_user_id, org_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Get query parameters for filtering
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    platform = request.args.get('platform')
    
    # Build query
    query = db.session.query(PostSchedule).join(Post).filter(Post.organization_id == org_id)
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(PostSchedule.scheduled_time >= start)
        except ValueError:
            return jsonify({'message': 'Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(PostSchedule.scheduled_time <= end)
        except ValueError:
            return jsonify({'message': 'Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    
    if platform:
        query = query.join(SocialAccount).filter(SocialAccount.platform == platform)
    
    # Get schedules
    schedules = query.order_by(PostSchedule.scheduled_time).all()
    
    # Build calendar data
    calendar_data = []
    for schedule in schedules:
        post = Post.query.get(schedule.post_id)
        social_account = SocialAccount.query.get(schedule.social_account_id)
        
        calendar_data.append({
            'id': schedule.id,
            'post_id': schedule.post_id,
            'post_content_type': post.content_type,
            'post_content': post.content,
            'social_account_id': schedule.social_account_id,
            'platform': social_account.platform,
            'account_name': social_account.account_name,
            'scheduled_time': schedule.scheduled_time.isoformat() if schedule.scheduled_time else None,
            'published_time': schedule.published_time.isoformat() if schedule.published_time else None,
            'status': schedule.status
        })
    
    return jsonify(calendar_data)

