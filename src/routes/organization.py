from flask import Blueprint, jsonify, request
from .auth import token_required
from src.models import db, Organization, OrganizationMember

organization_bp = Blueprint('organization', __name__, url_prefix='/api/organizations')


def is_org_member(user_id: int, org_id: int) -> bool:
    member = OrganizationMember.query.filter_by(user_id=user_id, organization_id=org_id).first()
    return member is not None


@organization_bp.route('', methods=['POST'])
@token_required
def create_organization(current_user_id):
    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'success': False, 'message': 'Missing name'}), 400
    org = Organization(name=name, description=description, owner_id=current_user_id)
    db.session.add(org)
    db.session.commit()
    # also add creator as member
    member = OrganizationMember(organization_id=org.id, user_id=current_user_id, role='owner')
    db.session.add(member)
    db.session.commit()
    return jsonify({'success': True, 'organization': org.to_dict()}), 201


@organization_bp.route('', methods=['GET'])
@token_required
def get_organizations(current_user_id):
    orgs = Organization.query.filter_by(owner_id=current_user_id).all()
    return jsonify({'success': True, 'organizations': [o.to_dict() for o in orgs]}), 200

__all__ = ['organization_bp', 'is_org_member']
