from flask import Blueprint

# Create main API blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# Import all routes from sub-files
from . import users, salons, staff, services, appointments
