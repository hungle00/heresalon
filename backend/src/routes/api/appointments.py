from flask import Blueprint, jsonify, request
from flask import current_app
from datetime import datetime, date, time
import re

from src.models import Appointment
from src.routes.api.auth import token_required, optional_token_required
from src.services.appointment_service import AppointmentService

blueprint = Blueprint('appointments', __name__, url_prefix='/api')

@blueprint.route('/appointments/', methods=['GET'])
@token_required
def get_appointments(current_user):
    """Get all appointments for current user"""
    try:
        appointments = AppointmentService.get_appointments(current_user.id)
        
        return jsonify([appointment.to_dict() for appointment in appointments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blueprint.route('/appointments/', methods=['POST'])
@optional_token_required
def create_appointment(current_user):
    """Create a new appointment for both authenticated and guest users"""
    data = request.get_json()
    
    try:
        user_id = current_user.id if current_user else None
        appointment, error = AppointmentService.create_appointment(data, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(appointment.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blueprint.route('/appointments/<int:appointment_id>/', methods=['GET'])
@token_required
def get_appointment(current_user, appointment_id):
    """Get appointment by ID"""
    try:
        appointment, error = AppointmentService.get_appointment_by_id(
            appointment_id, current_user.id
        )
        
        if error:
            if 'not found' in error.lower():
                return jsonify({'error': error}), 404
            elif 'access denied' in error.lower():
                return jsonify({'error': error}), 403
            else:
                return jsonify({'error': error}), 400
        
        return jsonify(appointment.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blueprint.route('/appointments/<int:appointment_id>/', methods=['PUT'])
@token_required
def update_appointment(current_user, appointment_id):
    """Update appointment"""
    data = request.get_json()
    
    try:
        appointment, error = AppointmentService.update_appointment(
            appointment_id, data, current_user.id
        )
        
        if error:
            if 'not found' in error.lower():
                return jsonify({'error': error}), 404
            elif 'access denied' in error.lower():
                return jsonify({'error': error}), 403
            else:
                return jsonify({'error': error}), 400
        
        return jsonify(appointment.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blueprint.route('/appointments/<int:appointment_id>/', methods=['DELETE'])
@token_required
def delete_appointment(current_user, appointment_id):
    """Delete appointment"""
    try:
        success, error = AppointmentService.delete_appointment(
            appointment_id, current_user.id
        )
        
        if not success:
            if 'not found' in error.lower():
                return jsonify({'error': error}), 404
            elif 'access denied' in error.lower():
                return jsonify({'error': error}), 403
            else:
                return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Appointment deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



