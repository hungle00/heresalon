from flask import Blueprint, jsonify, request
from src.models import Appointment
from src.models.appointment import AppointmentStatus
from datetime import datetime, date

blueprint = Blueprint('appointments', __name__, url_prefix='/api')

@blueprint.route('/appointments/', methods=['GET'])
def get_appointments():
    """Get all appointments"""
    appointments = Appointment.list()
    return jsonify([appointment.to_dict() for appointment in appointments])

@blueprint.route('/appointments/', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    data = request.get_json()
    
    required_fields = ['staff_id', 'user_id', 'service_id', 'date', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All required fields must be provided'}), 400
    
    try:
        appointment = Appointment.create(
            staff_id=data['staff_id'],
            user_id=data['user_id'],
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
def get_appointment(appointment_id):
    """Get appointment by ID"""
    appointment = Appointment.get(id=appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    return jsonify(appointment.to_dict())

@blueprint.route('/appointments/<int:appointment_id>/', methods=['PUT'])
def update_appointment(appointment_id):
    """Update appointment"""
    appointment = Appointment.get(id=appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    
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
def delete_appointment(appointment_id):
    """Delete appointment"""
    appointment = Appointment.get(id=appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404
    
    appointment.delete()
    return jsonify({'message': 'Appointment deleted successfully'}) 