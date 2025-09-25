from .counter import blueprint as counter
from .admin_auth import admin_auth_bp

# Import blueprint arrays
from .api import api_blueprints
from .admin import admin_blueprints

# Array of all main blueprints
main_blueprints = [
    counter,
    admin_auth_bp
] + api_blueprints + admin_blueprints

# Export for easy importing
__all__ = main_blueprints
