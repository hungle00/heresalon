from flask import Blueprint, render_template
from src.models import User, Salon, Staff, Service, Appointment
from src.models.appointment import AppointmentStatus
from src.routes.admin_auth import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required
def dashboard():
    """Admin dashboard"""
    stats = {
        'total_users': User.query.count(),
        'total_salons': Salon.query.count(),
        'total_staff': Staff.query.count(),
        'total_services': Service.query.count(),
        'total_appointments': Appointment.query.count(),
        'pending_appointments': Appointment.query.filter_by(status=AppointmentStatus.PENDING).count()
    }
    return render_template('admin/dashboard.html', stats=stats)
