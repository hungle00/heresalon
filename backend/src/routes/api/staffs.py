from flask import Blueprint, jsonify, request
from src.models import Staff, Salon
from src.models.staff import Seniority

blueprint = Blueprint('staff', __name__, url_prefix='/api')

@blueprint.route('/salons/<int:salon_id>/staffs/', methods=['GET'])
def get_salon_staff(salon_id):
    """Get all staff for a specific salon"""
    # Verify salon exists
    salon = Salon.get(id=salon_id)
    if not salon:
        return jsonify({'error': 'Salon not found'}), 404
    
    # Get staff for the salon
    staff = Staff.query.filter_by(salon_id=salon_id).all()
    return jsonify([member.to_dict() for member in staff])

@blueprint.route('/staffs/<int:staff_id>/', methods=['GET'])
def get_staff_member(staff_id):
    """Get staff member by ID"""
    staff = Staff.get(id=staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    return jsonify(staff.to_dict())

@blueprint.route('/staffs/<int:staff_id>/', methods=['PUT'])
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