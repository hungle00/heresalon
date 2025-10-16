# Import all admin blueprints
from .dashboard import blueprint as admin_dashboard_bp
from .users import blueprint as admin_users_bp
from .salons import blueprint as admin_salons_bp
from .staff import blueprint as admin_staff_bp
from .services import blueprint as admin_services_bp
from .appointments import blueprint as admin_appointments_bp

# Rename blueprints to avoid conflicts
admin_dashboard_bp.name = 'admin_dashboard'
admin_users_bp.name = 'admin_users'
admin_salons_bp.name = 'admin_salons'
admin_staff_bp.name = 'admin_staff'
admin_services_bp.name = 'admin_services'
admin_appointments_bp.name = 'admin_appointments'

# Array of all admin blueprints
admin_blueprints = [
    admin_dashboard_bp,
    admin_users_bp,
    admin_salons_bp,
    admin_staff_bp,
    admin_services_bp,
    admin_appointments_bp
]

# Export for easy importing
__all__ = admin_blueprints
