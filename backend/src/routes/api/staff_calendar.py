from flask import Blueprint, jsonify, request
from flask import current_app
from datetime import datetime, date

from src.models import Appointment, Staff, Service, User
from src.models.appointment import AppointmentStatus

blueprint = Blueprint('calendar', __name__, url_prefix='/api')

@blueprint.route('/staffs/<int:staff_id>/appointments/', methods=['GET'])
def get_staff_appointments(staff_id):
    """Get all appointments for a specific staff member with optional month filter"""
    
    # Check if staff exists
    staff = Staff.get(id=staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    
    # Get month filter from query parameters
    month = request.args.get('month')
    year = request.args.get('year')
    
    # Build query
    query = Appointment.query.filter_by(staff_id=staff_id)
    
    # Apply month filter if provided
    if month and year:
        try:
            month_int = int(month)
            year_int = int(year)
            
            # Filter by month and year
            from sqlalchemy import and_, extract
            query = query.filter(
                and_(
                    extract('month', Appointment.date) == month_int,
                    extract('year', Appointment.date) == year_int
                )
            )
        except ValueError:
            return jsonify({'error': 'Invalid month or year format'}), 400
    elif month:
        try:
            month_int = int(month)
            current_year = datetime.now().year
            from sqlalchemy import and_, extract
            query = query.filter(
                and_(
                    extract('month', Appointment.date) == month_int,
                    extract('year', Appointment.date) == current_year
                )
            )
        except ValueError:
            return jsonify({'error': 'Invalid month format'}), 400
    
    # Get appointments
    appointments = query.order_by(Appointment.date, Appointment.start_time).all()
    
    # Format response with additional staff and service information
    result = []
    for appointment in appointments:
        appointment_dict = appointment.to_dict()
        
        # Add service information
        service = Service.get(id=appointment.service_id)
        if service:
            appointment_dict['service'] = {
                'id': service.id,
                'name': service.name,
                'price': float(service.price) if service.price else None
            }
        
        # Add user information
        user = User.get(id=appointment.user_id)
        if user:
            appointment_dict['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        
        result.append(appointment_dict)
    
    return jsonify({
        'staff_id': staff_id,
        'staff_name': staff.name,
        'month': month,
        'year': year,
        'total_appointments': len(result),
        'appointments': result
    })

def get_available_time_slots(staff_id, date):
    """Get available time slots for a specific staff member on a specific date"""
    staff = Staff.get(id=staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    
    available_time_slots = AvailabilityService.get_available_time_slots(staff_id, date)
    return jsonify(available_time_slots)
