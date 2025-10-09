from flask import Blueprint, jsonify, request
from flask import current_app
from datetime import datetime, date, time
import re

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
        # Parse date
        appointment_date = date.fromisoformat(data['date'])
        
        # Parse time strings (e.g., "10:00", "11:30")
        start_time_str = data['start_time']
        end_time_str = data['end_time']
        
        # Validate time format (HH:MM)
        if validate_times_format(start_time_str) is False:
            return jsonify({'error': 'Invalid start_time format. Use HH:MM (e.g., 10:00)'}), 400
            
        if validate_times_format(end_time_str) is False:
            return jsonify({'error': 'Invalid end_time format. Use HH:MM (e.g., 11:30)'}), 400
        
        # Parse time strings to time objects
        start_time_obj = time.fromisoformat(start_time_str)
        end_time_obj = time.fromisoformat(end_time_str)
        
        # Validate that start_time is earlier than end_time
        if start_time_obj >= end_time_obj:
            return jsonify({'error': 'start_time must be earlier than end_time'}), 400
        
        # Combine date and time to create datetime objects
        start_datetime = datetime.combine(appointment_date, start_time_obj)
        end_datetime = datetime.combine(appointment_date, end_time_obj)
        
        # Create appointment
        appointment = Appointment.create(
            staff_id=data['staff_id'],
            user_id=current_user.id,
            service_id=data['service_id'],
            status=AppointmentStatus(data.get('status', 'pending')),
            date=appointment_date,
            start_time=start_datetime,
            end_time=end_datetime
        )
        return jsonify(appointment.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date or time format: {str(e)}'}), 400
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
            start_time_str = data['start_time']
            if validate_times_format(start_time_str) is False:
                return jsonify({'error': 'Invalid start_time format. Use HH:MM (e.g., 10:00)'}), 400
            
            start_time_obj = time.fromisoformat(start_time_str)
            start_datetime = datetime.combine(appointment.date, start_time_obj)
            appointment.start_time = start_datetime
            
        if 'end_time' in data:
            end_time_str = data['end_time']
            if validate_times_format(end_time_str) is False:
                return jsonify({'error': 'Invalid end_time format. Use HH:MM (e.g., 11:30)'}), 400
            
            end_time_obj = time.fromisoformat(end_time_str)
            end_datetime = datetime.combine(appointment.date, end_time_obj)
            appointment.end_time = end_datetime
        
        # Validate that start_time is earlier than end_time
        if appointment.start_time >= appointment.end_time:
            return jsonify({'error': 'start_time must be earlier than end_time'}), 400
        
        appointment.save()
        return jsonify(appointment.to_dict())
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date or time format: {str(e)}'}), 400
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

def validate_times_format(time_str):
    """Validate time format (HH:MM)"""
    time_pattern = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
    return re.match(time_pattern, time_str) is not None
