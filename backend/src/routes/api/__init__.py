# Import all API blueprints
from .users import blueprint as api_users_bp
from .salons import blueprint as api_salons_bp
from .staffs import blueprint as api_staffs_bp
from .services import blueprint as api_services_bp
from .appointments import blueprint as api_appointments_bp

# Rename blueprints to avoid conflicts
api_users_bp.name = 'api_users'
api_salons_bp.name = 'api_salons'
api_staffs_bp.name = 'api_staffs'
api_services_bp.name = 'api_services'
api_appointments_bp.name = 'api_appointments'

# Array of all API blueprints
api_blueprints = [
    api_users_bp,
    api_salons_bp,
    api_staffs_bp,
    api_services_bp,
    api_appointments_bp
]

# Export for easy importing
__all__ = api_blueprints
