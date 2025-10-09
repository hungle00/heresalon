from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

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

        # Configure CORS with more permissive settings for development
        CORS(self.flask_app, 
             origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
             allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
             supports_credentials=True,
             send_wildcard=True)

        # Register all blueprints using the main_blueprints array
        for blueprint in routes.main_blueprints:
            self.flask_app.register_blueprint(blueprint)

        # Init Celery
        self.celery = make_celery(self.flask_app)

        # Init Flask-SQLAlchemy
        self.db = db
        self.db.init_app(self.flask_app)

        # Init Flask-Migrate
        # u.wait_for_service('postgres', 5432, timeout=30.0)
        self.migrate = Migrate(self.flask_app, self.db)

    def init_routes(self):

        @self.flask_app.route('/')
        def home():
            return {'message': 'Heresalon API', 'status': 'running'}

        @self.flask_app.route('/health')
        def health():
            return {'status': 'healthy', 'message': 'API is running'}

    def run(self):
        """Run the application"""
        self.flask_app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    Application.boot()
