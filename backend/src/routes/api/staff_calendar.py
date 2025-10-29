from flask import Blueprint, jsonify, request
from flask import current_app
from datetime import datetime, date

from src.models import Appointment, Staff, Service, User
from src.models.appointment import AppointmentStatus
from src.services.availability_service import AvailabilityService

blueprint = Blueprint('calendar', __name__, url_prefix='/api')

@blueprint.route('/staffs/<int:staff_id>/appointments/', methods=['GET'])
def get_appointments(staff_id):
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

@blueprint.route('/staffs/<int:staff_id>/available-time-slots/', methods=['GET'])
def get_available_time_slots(staff_id):
    """Get available time slots for a specific staff member on a specific date"""
    # Check if staff exists
    staff = Staff.get(id=staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    
    # Get date parameter from query string
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date parameter is required'}), 400
    
    try:
        # Parse date string (expected format: YYYY-MM-DD)
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Get optional parameters
    service_duration = request.args.get('service_duration', 60, type=int)
    
    # Get available time slots
    available_time_slots = AvailabilityService.get_available_time_slots(
        staff_id=staff_id,
        appointment_date=appointment_date,
        service_duration_minutes=service_duration
    )
    
    return jsonify({
        'staff_id': staff_id,
        'date': appointment_date.isoformat(),
        'available_slots': available_time_slots,
        'total_slots': len(available_time_slots)
    })
