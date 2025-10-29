from flask import Blueprint, render_template, session
from src.models import User, Salon, Staff, Service, Appointment
from src.models.appointment import AppointmentStatus
from src.models.user import UserRole
from src.routes.admin_auth import manager_or_admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@manager_or_admin_required
def dashboard():
    """Admin dashboard"""
    # Get current user
    current_user = User.get(id=session['admin_id'])
    
    if current_user.is_admin:
        # Admin sees general stats
        stats = {
            'total_users': User.query.count(),
            'total_salons': Salon.query.count(),
            'total_staff': Staff.query.count(),
            'total_services': Service.query.count(),
            'total_appointments': Appointment.query.count(),
            'pending_appointments': Appointment.query.filter_by(status=AppointmentStatus.PENDING).count()
        }
    else:
        # Manager sees salon-specific stats
        if not current_user.salon_id:
            stats = {
                'total_users': 0,
                'total_salons': 0,
                'total_staff': 0,
                'total_services': 0,
                'total_appointments': 0,
                'pending_appointments': 0
            }
        else:
            # Get salon info
            salon = Salon.get(id=current_user.salon_id)
            stats = {
                'salon_name': salon.name if salon else 'Unknown Salon',
                'salon_id': current_user.salon_id,
                'total_staff': Staff.query.filter_by(salon_id=current_user.salon_id).count(),
                'total_services': Service.query.filter_by(salon_id=current_user.salon_id).count(),
                'total_appointments': Appointment.query.join(Staff).filter(Staff.salon_id == current_user.salon_id).count(),
                'pending_appointments': Appointment.query.join(Staff).filter(
                    Staff.salon_id == current_user.salon_id,
                    Appointment.status == AppointmentStatus.PENDING
                ).count(),
                'confirmed_appointments': Appointment.query.join(Staff).filter(
                    Staff.salon_id == current_user.salon_id,
                    Appointment.status == AppointmentStatus.CONFIRMED
                ).count(),
                'completed_appointments': Appointment.query.join(Staff).filter(
                    Staff.salon_id == current_user.salon_id,
                    Appointment.status == AppointmentStatus.COMPLETED
                ).count()
            }
    
    return render_template('admin/dashboard.html', stats=stats, current_user=current_user)
