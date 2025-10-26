from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from src.models import Salon
from src.routes.admin_auth import admin_required, manager_or_admin_required
from flask import session
from src.models.user import User, UserRole

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
    if current_user and current_user.role == UserRole.MANAGER:
        if current_user.salon_id != salon_id:
            abort(403)  # Forbidden - manager can only view their own salon
    
    return render_template('admin/salons/salon_detail.html', salon=salon)

@blueprint.route('/salons/<int:salon_id>/edit', methods=['GET', 'POST'])
@manager_or_admin_required
def edit_salon(salon_id):
    """Edit salon information."""
    salon = Salon.query.get_or_404(salon_id)
    
    current_user = User.query.filter_by(username=session.get('admin_username')).first()
    if current_user and current_user.role == UserRole.MANAGER:
        if current_user.salon_id != salon_id:
            abort(403)  # Forbidden - manager can only edit their own salon
    
    if request.method == 'POST':
        try:
            # Update salon information
            salon.name = request.form.get('name', salon.name)
            salon.address = request.form.get('address', salon.address)
            salon.description = request.form.get('description', salon.description)
            
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
            # Create a new salon
            salon = Salon(
                name=request.form.get('name'),
                address=request.form.get('address'),
                description=request.form.get('description')
            )
            
            salon.save()
            flash('Salon created successfully!', 'success')
            return redirect(url_for('admin_salons.salon_detail', salon_id=salon.id))
            
        except Exception as e:
            flash(f'Error creating salon: {str(e)}', 'error')
    
    return render_template('admin/salons/salon_form.html', salon=None, is_edit=False)
