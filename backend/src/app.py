from flask import Flask
from flask_migrate import Migrate

from src import routes, utils as u
from src.models import db
from src.settings import Settings as S
from src.tasks import make_celery


class Application:

    @classmethod
    def boot(cls):
        """Begin the application"""
        app = cls()
        app.run()
        return app

    def __init__(self):
        self.init_flask()
        self.init_routes()

    def init_flask(self):
        # Init Flask
        self.flask_app = Flask(__name__, static_url_path='/static')
        self.flask_app.config.from_object(S)

        # Register the admin routes
        admin_routes = [
            routes.admin.dashboard.dashboard_bp,
            routes.admin.users.user_bp
        ]
        for route in admin_routes:
            self.flask_app.register_blueprint(route)

        # Register the api routes
        self.flask_app.register_blueprint(routes.api_blueprint)

        # Register the public routes
        for blueprint in [routes.counter, routes.localstack]:
            self.flask_app.register_blueprint(blueprint)

        # Init Celery
        self.celery = make_celery(self.flask_app)

        # Init Flask-SQLAlchemy
        self.db = db
        self.db.init_app(self.flask_app)

        # Init Flask-Migrate
        self.migrate = Migrate(self.flask_app, self.db)

    def init_routes(self):

        @self.flask_app.route('/')
        def home(key):
            return 'home'
