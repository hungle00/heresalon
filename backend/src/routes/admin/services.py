from flask import Blueprint, render_template, request, redirect, url_for, flash
from decimal import Decimal
from src.models import Service
from src.models.service import ServiceType
from src.routes.admin_auth import admin_required

blueprint = Blueprint('admin_services', __name__, url_prefix='/admin')

@blueprint.route('/services/')
@admin_required
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
    
    return render_template('admin/services.html', 
                         services=services,
                         ServiceType=ServiceType)
