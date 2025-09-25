# Import all routes directly into main blueprint
from .dashboard import dashboard_bp
from .users import user_bp

# Export blueprints
__all__ = ['dashboard_bp', 'user_bp']