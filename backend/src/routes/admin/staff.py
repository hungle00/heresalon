from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models import Staff, Salon
from src.models.staff import StaffRole, Seniority
from src.routes.admin_auth import manager_or_admin_required

blueprint = Blueprint('admin_staff', __name__, url_prefix='/admin')

@blueprint.route('/staff/')
@manager_or_admin_required
def staff():
    """List all staff members."""
    # Get filter parameters
    salon_id = request.args.get('salon_id', type=int)
    role = request.args.get('role')
    seniority = request.args.get('seniority')
    search = request.args.get('search')
    
    staff_members = Staff.query.all()
    
    # Get salons for filter dropdown
    salons = Salon.query.all()
    
    return render_template('admin/staff.html', 
                         staff_members=staff_members, 
                         salons=salons,
                         StaffRole=StaffRole,
                         Seniority=Seniority)


