# Import all API blueprints
from .salons import blueprint as api_salons_bp
from .staffs import blueprint as api_staffs_bp
from .services import blueprint as api_services_bp
from .appointments import blueprint as api_appointments_bp
from .auth import blueprint as api_auth_bp
from .chat import blueprint as api_chat_bp

# Rename blueprints to avoid conflicts
api_salons_bp.name = 'api_salons'
api_staffs_bp.name = 'api_staffs'
api_services_bp.name = 'api_services'
api_appointments_bp.name = 'api_appointments'
api_auth_bp.name = 'api_auth'

# Array of all API blueprints
api_blueprints = [
    api_salons_bp,
    api_staffs_bp,
    api_services_bp,
    api_appointments_bp,
    api_auth_bp,
    api_chat_bp
]

# Export for easy importing
__all__ = api_blueprints
