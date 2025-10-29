from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models import Staff, Salon, User
from src.models.staff import StaffRole, Seniority
from src.models.user import UserRole
from src.routes.admin_auth import manager_or_admin_required

blueprint = Blueprint('admin_staff', __name__, url_prefix='/admin')

@blueprint.route('/staff/')
@manager_or_admin_required
def staff():
    """List all staff members."""
    # Get current user
    current_user = User.get(id=session['admin_id'])
    
    # Get filter parameters
    salon_id = request.args.get('salon_id', type=int)
    role = request.args.get('role')
    seniority = request.args.get('seniority')
    search = request.args.get('search')
    
    # Build query based on user role
    if current_user.is_admin:
        # Admin can see all staff
        staff_members = Staff.query
        salons = Salon.query.all()
    else:
        # Manager can only see staff from their managed salon
        # Use User.salon_id directly (managers must have salon_id)
        if not current_user.salon_id:
            flash('Manager must be assigned to a salon!', 'error')
            return redirect(url_for('admin_dashboard.dashboard'))
        
        staff_members = Staff.query.filter_by(salon_id=current_user.salon_id)
        salons = Salon.query.filter_by(id=current_user.salon_id).all()
    
    
    staff_members = staff_members.all()
    
    return render_template('admin/staff/staff.html', 
                         staff_members=staff_members, 
                         salons=salons,
                         StaffRole=StaffRole,
                         Seniority=Seniority)

@blueprint.route('/staff/new/', methods=['GET', 'POST'])
@manager_or_admin_required
def new_staff():
    """Create new staff member"""
    # Get current user
    current_user = User.get(id=session['admin_id'])
    
    # Only managers can create staff
    if current_user.is_admin:
        flash('Only managers can create staff members!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    # Manager must have salon_id
    if not current_user.salon_id:
        flash('Manager must be assigned to a salon!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    salons = Salon.query.filter_by(id=current_user.salon_id).all()
    
    if request.method == 'POST':
        try:
            salon_id = int(request.form['salon_id'])
            
            # For manager, ensure they can only create staff in their salon
            if current_user.role != UserRole.ADMIN:
                if salon_id != current_user.salon_id:
                    flash('You can only create staff in your managed salon!', 'error')
                    return redirect(url_for('admin_staff.new_staff'))
            
            # Convert string to Seniority enum
            seniority = Seniority(request.form.get('seniority')) if request.form.get('seniority') else None
            
            staff = Staff.create(
                name=request.form['name'],
                role=int(request.form['role']),
                salon_id=salon_id,
                seniority=seniority,
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
    # Get current user
    current_user = User.get(id=session['admin_id'])
    
    # Only managers can edit staff
    if current_user.is_admin:
        flash('Only managers can edit staff members!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    staff = Staff.get(id=staff_id)
    if not staff:
        flash('Staff member not found!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    # Check if manager can edit this staff
    if not current_user.salon_id or staff.salon_id != current_user.salon_id:
        flash('You can only edit staff in your managed salon!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    # Manager can only assign staff to their salon
    salons = Salon.query.filter_by(id=current_user.salon_id).all()
    
    if request.method == 'POST':
        try:
            salon_id = int(request.form['salon_id'])
            
            # For manager, ensure they can only assign staff to their salon
            if current_user.role != UserRole.ADMIN:
                if salon_id != current_user.salon_id:
                    flash('You can only assign staff to your managed salon!', 'error')
                    return redirect(url_for('admin_staff.edit_staff', staff_id=staff_id))
            
            seniority = Seniority(request.form['seniority'])
            staff.name = request.form['name']
            staff.role = int(request.form['role'])
            staff.salon_id = salon_id
            staff.seniority = seniority
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
    # Get current user
    current_user = User.get(id=session['admin_id'])
    
    # Only managers can delete staff
    if current_user.is_admin:
        flash('Only managers can delete staff members!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    staff = Staff.get(id=staff_id)
    if not staff:
        flash('Staff member not found!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    # Check if manager can delete this staff
    if not current_user.salon_id or staff.salon_id != current_user.salon_id:
        flash('You can only delete staff in your managed salon!', 'error')
        return redirect(url_for('admin_staff.staff'))
    
    try:
        staff.delete()
        flash('Staff member deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting staff member: {str(e)}', 'error')
    
    return redirect(url_for('admin_staff.staff'))


