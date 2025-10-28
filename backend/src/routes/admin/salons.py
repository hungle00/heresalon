from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from src.models import Salon
from src.routes.admin_auth import admin_required, manager_or_admin_required
from flask import session
from src.models.user import User, UserRole
from datetime import time

blueprint = Blueprint('admin_salons', __name__, url_prefix='/admin')

@blueprint.route('/salons/')
@admin_required
def salons():
    """List all salons."""
    salons = Salon.query.all()
    
    return render_template('admin/salons/salons.html', salons=salons)

@blueprint.route('/salons/<int:salon_id>')
@manager_or_admin_required
def salon_detail(salon_id):
    """View salon details by ID."""
    salon = Salon.query.get_or_404(salon_id)
    
    current_user = User.query.filter_by(username=session.get('admin_username')).first()
    if current_user and current_user.is_manager:
        if current_user.salon_id != salon_id:
            abort(403)  # Forbidden - manager can only view their own salon
    
    return render_template('admin/salons/salon_detail.html', salon=salon)

@blueprint.route('/salons/<int:salon_id>/edit', methods=['GET', 'POST'])
@manager_or_admin_required
def edit_salon(salon_id):
    """Edit salon information."""
    salon = Salon.query.get_or_404(salon_id)
    
    current_user = User.query.filter_by(username=session.get('admin_username')).first()
    if current_user and current_user.is_manager:
        if current_user.salon_id != salon_id:
            abort(403)  # Forbidden - manager can only edit their own salon
    
    if request.method == 'POST':
        try:
            # Update salon information
            salon.name = request.form.get('name', salon.name)
            salon.address = request.form.get('address', salon.address)
            salon.description = request.form.get('description', salon.description)
            
            # Handle working time fields
            start_time_str = request.form.get('start_working_time')
            end_time_str = request.form.get('end_working_time')
            
            if start_time_str:
                salon.start_working_time = time.fromisoformat(start_time_str)
            else:
                salon.start_working_time = None
                
            if end_time_str:
                salon.end_working_time = time.fromisoformat(end_time_str)
            else:
                salon.end_working_time = None
            
            salon.save()
            flash('Salon updated successfully!', 'success')
            return redirect(url_for('admin_salons.salon_detail', salon_id=salon.id))
            
        except Exception as e:
            flash(f'Error updating salon: {str(e)}', 'error')
    
    return render_template('admin/salons/salon_form.html', salon=salon, is_edit=True)

@blueprint.route('/salons/new', methods=['GET', 'POST'])
@admin_required
def new_salon():
    """Add a new salon - only admin can access."""
    if request.method == 'POST':
        try:
            # Handle working time fields
            start_time_str = request.form.get('start_working_time')
            end_time_str = request.form.get('end_working_time')
            
            start_time = None
            end_time = None
            
            if start_time_str:
                start_time = time.fromisoformat(start_time_str)
            if end_time_str:
                end_time = time.fromisoformat(end_time_str)
            
            # Create a new salon
            salon = Salon(
                name=request.form.get('name'),
                address=request.form.get('address'),
                description=request.form.get('description'),
                start_working_time=start_time,
                end_working_time=end_time
            )
            
            salon.save()
            flash('Salon created successfully!', 'success')
            return redirect(url_for('admin_salons.salon_detail', salon_id=salon.id))
            
        except Exception as e:
            flash(f'Error creating salon: {str(e)}', 'error')
    
    return render_template('admin/salons/salon_form.html', salon=None, is_edit=False)
