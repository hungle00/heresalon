from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models import Salon
from src.routes.admin_auth import admin_required

blueprint = Blueprint('admin_salons', __name__, url_prefix='/admin')

@blueprint.route('/salons/')
@admin_required
def salons():
    """List all salons."""
    salons = Salon.query.all()
    
    return render_template('admin/salons/salons.html', salons=salons)
