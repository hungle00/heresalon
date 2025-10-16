from flask import Blueprint, render_template, request, redirect, url_for, flash
from decimal import Decimal
from src.models import Service
from src.models.service import ServiceType
from src.routes.admin_auth import manager_or_admin_required

blueprint = Blueprint('admin_services', __name__, url_prefix='/admin')

@blueprint.route('/services/')
@manager_or_admin_required
def services():
    """List all services."""
    # Get filter parameters
    service_type = request.args.get('type')
    search = request.args.get('search')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Build query
    query = Service.query
    
    if service_type:
        query = query.filter(Service.type == service_type)
    
    if search:
        query = query.filter(Service.name.contains(search))
    
    if min_price is not None:
        query = query.filter(Service.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Service.price <= max_price)
    
    services = query.all()
    
    return render_template('admin/services/services.html', 
                         services=services,
                         ServiceType=ServiceType)

@blueprint.route('/services/new/', methods=['GET', 'POST'])
@manager_or_admin_required
def new_service():
    """Create new service"""
    if request.method == 'POST':
        try:
            service = Service.create(
                name=request.form['name'],
                type=request.form['type'],
                price=Decimal(request.form['price']),
                duration=int(request.form['duration']),
                description=request.form.get('description', ''),
                is_active=request.form.get('is_active') == 'on'
            )
            flash('Service created successfully!', 'success')
            return redirect(url_for('admin_services.services'))
        except Exception as e:
            flash(f'Error creating service: {str(e)}', 'error')
    
    return render_template('admin/services/service_form.html', service=None, ServiceType=ServiceType)

@blueprint.route('/services/<int:service_id>/edit/', methods=['GET', 'POST'])
@manager_or_admin_required
def edit_service(service_id):
    """Edit service"""
    service = Service.get(id=service_id)
    if not service:
        flash('Service not found!', 'error')
        return redirect(url_for('admin_services.services'))
    
    if request.method == 'POST':
        try:
            service.name = request.form['name']
            service.type = request.form['type']
            service.price = Decimal(request.form['price'])
            service.duration = int(request.form['duration'])
            service.description = request.form.get('description', '')
            service.is_active = request.form.get('is_active') == 'on'
            service.save()
            flash('Service updated successfully!', 'success')
            return redirect(url_for('admin_services.services'))
        except Exception as e:
            flash(f'Error updating service: {str(e)}', 'error')
    
    return render_template('admin/services/service_form.html', service=service, ServiceType=ServiceType)

@blueprint.route('/services/<int:service_id>/delete/', methods=['POST'])
@manager_or_admin_required
def delete_service(service_id):
    """Delete service"""
    service = Service.get(id=service_id)
    if not service:
        flash('Service not found!', 'error')
        return redirect(url_for('admin_services.services'))
    
    try:
        service.delete()
        flash('Service deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting service: {str(e)}', 'error')
    
    return redirect(url_for('admin_services.services'))
