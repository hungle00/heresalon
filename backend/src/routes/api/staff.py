from flask import Blueprint, jsonify, request
from src.models import Staff
from src.models.staff import Seniority

blueprint = Blueprint('staff', __name__)

@blueprint.route('/staff/', methods=['GET'])
def get_staff():
    """Get all staff"""
    staff = Staff.list()
    return jsonify([member.to_dict() for member in staff])

@blueprint.route('/staff/<int:staff_id>/', methods=['GET'])
def get_staff_member(staff_id):
    """Get staff member by ID"""
    staff = Staff.get(id=staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    return jsonify(staff.to_dict())

@blueprint.route('/staff/<int:staff_id>/', methods=['PUT'])
def update_staff(staff_id):
    """Update staff member"""
    staff = Staff.get(id=staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'name' in data:
            staff.name = data['name']
        if 'bio' in data:
            staff.bio = data['bio']
        if 'role' in data:
            staff.role = data['role']
        if 'years_experience' in data:
            staff.years_experience = data['years_experience']
        if 'seniority' in data:
            staff.seniority = Seniority(data['seniority']) if data['seniority'] else None
        if 'rating' in data:
            staff.rating = data['rating']
        if 'specialties' in data:
            staff.specialties = data['specialties']
        if 'image_url' in data:
            staff.image_url = data['image_url']
        
        staff.save()
        return jsonify(staff.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
