from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from src.models import db, Appointment, User, Staff, Service, Salon
from src.models.appointment import AppointmentStatus
from src.models.user import UserRole
from datetime import datetime, date, timedelta
from sqlalchemy import and_, or_
from src.routes.admin_auth import manager_or_admin_required

blueprint = Blueprint('admin_appointments', __name__, url_prefix='/admin/appointments')

@blueprint.route('/')
@manager_or_admin_required
def index():
    """Display all appointments with filtering and pagination."""
    from flask import session
    from src.models import User
    
    # Get current user
    current_user = User.get(id=session['admin_id'])
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter parameters
    status_filter = request.args.get('status', '')
    date_filter = request.args.get('date', '')
    staff_filter = request.args.get('staff', '')
    search = request.args.get('search', '')
    
    # Build query based on user role
    if current_user.is_admin:
        # Admin sees all appointments
        query = Appointment.query.join(Staff).outerjoin(User).join(Service)
    else:
        # Manager sees only appointments from their salon
        if not current_user.salon_id:
            flash('Manager must be assigned to a salon!', 'error')
            return redirect(url_for('admin_dashboard.dashboard'))
        
        query = Appointment.query.join(Staff).filter(Staff.salon_id == current_user.salon_id).outerjoin(User).join(Service)
    
    # Apply filters
    if status_filter:
        query = query.filter(Appointment.status == status_filter)
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(Appointment.date == filter_date)
        except ValueError:
            pass
    
    if staff_filter:
        query = query.filter(Staff.id == staff_filter)
    
    if search:
        query = query.filter(
            or_(
                User.username.ilike(f'%{search}%'),
                Staff.name.ilike(f'%{search}%'),
                Service.name.ilike(f'%{search}%'),
                Appointment.phone_number.ilike(f'%{search}%')
            )
        )
    
    # Order by date and time
    query = query.order_by(Appointment.date.desc(), Appointment.start_time.desc())
    
    # Paginate
    appointments = query.all()
    
    # Get filter options based on user role
    if current_user.is_admin:
        staffs = Staff.query.all()
    else:
        staffs = Staff.query.filter_by(salon_id=current_user.salon_id).all()
    
    statuses = [status.value for status in AppointmentStatus]
    
    return render_template('admin/appointments/appointments.html',
                         appointments=appointments,
                         staffs=staffs,
                         statuses=statuses,
                         current_filters={
                             'status': status_filter,
                             'date': date_filter,
                             'staff': staff_filter,
                             'search': search
                         })

@blueprint.route('/<int:appointment_id>')
@manager_or_admin_required
def view(appointment_id):
    """View appointment details."""
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('admin/appointments/appointment_detail.html', appointment=appointment)

@blueprint.route('/<int:appointment_id>/edit', methods=['GET', 'POST'])
def edit(appointment_id):
    """Edit appointment."""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if request.method == 'POST':
        try:
            # Update appointment data
            appointment.status = request.form.get('status')
            appointment.date = datetime.strptime(
                request.form.get('date'), '%Y-%m-%d'
            ).date()
            appointment.start_time = datetime.strptime(
                request.form.get('start_time'), '%Y-%m-%dT%H:%M'
            )
            appointment.end_time = datetime.strptime(
                request.form.get('end_time'), '%Y-%m-%dT%H:%M'
            )
            
            # Update staff if changed
            new_staff_id = request.form.get('staff_id')
            if new_staff_id:
                appointment.staff_id = new_staff_id
            
            # Update service if changed
            new_service_id = request.form.get('service_id')
            if new_service_id:
                appointment.service_id = new_service_id
            
            db.session.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('admin_appointments.view', appointment_id=appointment.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating appointment: {str(e)}', 'error')
    
    # Get options for dropdowns
    staffs = Staff.query.all()
    services = Service.query.all()
    statuses = [status.value for status in AppointmentStatus]
    
    return render_template('admin/appointments/appointment_edit.html',
                         appointment=appointment,
                         staffs=staffs,
                         services=services,
                         statuses=statuses)

@blueprint.route('/<int:appointment_id>/delete', methods=['POST'])
def delete(appointment_id):
    """Delete appointment."""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting appointment: {str(e)}', 'error')
    
    return redirect(url_for('admin_appointments.index'))

@blueprint.route('/<int:appointment_id>/status', methods=['PUT'])
@manager_or_admin_required
def update_status(appointment_id):
    """Update appointment status via AJAX."""
    appointment = Appointment.query.get_or_404(appointment_id)
    new_status = request.json.get('status')
    
    if new_status not in [status.value for status in AppointmentStatus]:
        return jsonify({'error': 'Invalid status'}), 400
    
    try:
        # Convert string to AppointmentStatus enum
        status_enum = AppointmentStatus(new_status)
        appointment.status = status_enum
        db.session.commit()
        return jsonify({
            'success': True,
            'status': appointment.status.value,
            'message': 'Status updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@blueprint.route('/calendar')
def calendar():
    """Display appointments in calendar view."""
    # Get date range (default to current month)
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    # Get appointments for the month
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    appointments = Appointment.query.filter(
        and_(
            Appointment.date >= start_date,
            Appointment.date < end_date
        )
    ).join(Staff).outerjoin(User).join(Service).all()
    
    # Get staff for filtering
    staffs = Staff.query.all()
    
    return render_template('admin/appointments/appointments_calendar.html',
                         appointments=appointments,
                         staffs=staffs,
                         current_year=year,
                         current_month=month)

