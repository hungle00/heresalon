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
    
    return render_template('admin/staff/staff.html', 
                         staff_members=staff_members, 
                         salons=salons,
                         StaffRole=StaffRole,
                         Seniority=Seniority)

@blueprint.route('/staff/new/', methods=['GET', 'POST'])
@manager_or_admin_required
def new_staff():
    """Create new staff member"""
    salons = Salon.query.all()
    
    if request.method == 'POST':
        try:
            staff = Staff.create(
                name=request.form['name'],
                role=int(request.form['role']),
                salon_id=int(request.form['salon_id']),
                seniority=request.form.get('seniority'),
                years_experience=int(request.form.get('experience_years', 0)) if request.form.get('experience_years') else None,
                specialties=request.form.get('specialization', ''),
                bio=request.form.get('bio', '')
            )
            flash('Staff member created successfully!', 'success')
            return redirect(url_for('admin_staff.staff'))
        except Exception as e:
            flash(f'Error creating staff member: {str(e)}', 'error')
    
    return render_template('admin/staff/staff_form.html', 
                         staff=None, 
                         salons=salons,
                         StaffRole=StaffRole,
                         Seniority=Seniority)

@blueprint.route('/staff/<int:staff_id>/edit/', methods=['GET', 'POST'])
@manager_or_admin_required
def edit_staff(staff_id):
    """Edit staff member"""
    staff = Staff.get(id=staff_id)
    if not staff:
        flash('Staff member not found!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    salons = Salon.query.all()
    
    if request.method == 'POST':
        try:
            staff.name = request.form['name']
            staff.role = int(request.form['role'])
            staff.salon_id = int(request.form['salon_id'])
            staff.seniority = request.form.get('seniority')
            staff.years_experience = int(request.form.get('experience_years', 0)) if request.form.get('experience_years') else None
            staff.specialties = request.form.get('specialization', '')
            staff.bio = request.form.get('bio', '')
            staff.save()
            flash('Staff member updated successfully!', 'success')
            return redirect(url_for('admin_staff.staff'))
        except Exception as e:
            flash(f'Error updating staff member: {str(e)}', 'error')
    
    return render_template('admin/staff/staff_form.html', 
                         staff=staff, 
                         salons=salons,
                         StaffRole=StaffRole,
                         Seniority=Seniority)

@blueprint.route('/staff/<int:staff_id>/delete/', methods=['POST'])
@manager_or_admin_required
def delete_staff(staff_id):
    """Delete staff member"""
    staff = Staff.get(id=staff_id)
    if not staff:
        flash('Staff member not found!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    try:
        staff.delete()
        flash('Staff member deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting staff member: {str(e)}', 'error')
    
    return redirect(url_for('admin_staff.staff'))


