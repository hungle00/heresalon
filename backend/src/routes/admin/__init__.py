# Import all admin blueprints
from .dashboard import blueprint as admin_dashboard_bp
from .users import blueprint as admin_users_bp

# Rename blueprints to avoid conflicts
admin_dashboard_bp.name = 'admin_dashboard'
admin_users_bp.name = 'admin_users'

# Array of all admin blueprints
admin_blueprints = [
    admin_dashboard_bp,
    admin_users_bp
]

# Export for easy importing
__all__ = admin_blueprints
