from flask import Blueprint, jsonify, request
from flask import current_app
from datetime import datetime, date

from src.models import Appointment
from src.models.appointment import AppointmentStatus
from src.routes.api.auth import token_required

blueprint = Blueprint('appointments', __name__, url_prefix='/api')

@blueprint.route('/appointments/', methods=['GET'])
@token_required
def get_appointments(current_user):
    """Get all appointments for current user"""
    # For customers, only show their own appointments
    # For staff/admin, show all appointments
    if current_user.role.value == 'customer':
        appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    else:
        appointments = Appointment.list()
    
    return jsonify([appointment.to_dict() for appointment in appointments])

@blueprint.route('/appointments/', methods=['POST'])
@token_required
def create_appointment(current_user):
    """Create a new appointment"""
    data = request.get_json()
    
    required_fields = ['staff_id', 'service_id', 'date', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All required fields must be provided'}), 400
    
    try:
        appointment = Appointment.create(
            staff_id=data['staff_id'],
            user_id=current_user.id,  # Use current user's ID
            service_id=data['service_id'],
            status=AppointmentStatus(data.get('status', 'pending')),
            date=date.fromisoformat(data['date']),
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time'])
        )
        return jsonify(appointment.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/appointments/<int:appointment_id>/', methods=['GET'])
@token_required
def get_appointment(current_user, appointment_id):
    """Get appointment by ID"""
    appointment = Appointment.get(id=appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    
    # Check if user can access this appointment
    if current_user.role.value == 'customer' and appointment.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(appointment.to_dict())

@blueprint.route('/appointments/<int:appointment_id>/', methods=['PUT'])
@token_required
def update_appointment(current_user, appointment_id):
    """Update appointment"""
    appointment = Appointment.get(id=appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    
    # Check if user can modify this appointment
    if current_user.role.value == 'customer' and appointment.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    try:
        if 'status' in data:
            appointment.status = AppointmentStatus(data['status'])
        if 'date' in data:
            appointment.date = date.fromisoformat(data['date'])
        if 'start_time' in data:
            appointment.start_time = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data:
            appointment.end_time = datetime.fromisoformat(data['end_time'])
        
        appointment.save()
        return jsonify(appointment.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/appointments/<int:appointment_id>/', methods=['DELETE'])
@token_required
def delete_appointment(current_user, appointment_id):
    """Delete appointment"""
    appointment = Appointment.get(id=appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    
    # Check if user can delete this appointment
    if current_user.role.value == 'customer' and appointment.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    appointment.delete()
    return jsonify({'message': 'Appointment deleted successfully'})
