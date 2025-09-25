import os


class Parse:
    """Class of utility functions to parse environment variables"""

    @staticmethod
    def bool(field):
        """Parse booleans (defaults to False)"""
        return os.getenv(field, '').lower() in ['true', '1']


class Settings:

    # General
    DEV = Parse.bool('DEV')
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_URL = f'redis://{REDIS_HOST}:6379'

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')

    # Database - Use absolute path to avoid confusion
    AES_SECRET_KEY = os.getenv('AES_SECRET_KEY', 'fake-aes-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.abspath("salon.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_CONFIG = {
        'beat_schedule': {
            'ping_once': {
                'task': 'src.tasks.ping_once',
                'args': (1,),
                'schedule': 5.0,
            },
        }
    }
