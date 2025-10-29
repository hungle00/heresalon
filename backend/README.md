# Salon Management Backend

A Flask-based REST API and admin interface for salon management system.

## Features
This Flask application includes 2 main components:

- **Admin Interface**: Web-based admin panel with templates
- **API Endpoints**: RESTful API for React frontend

## Tech Stack

- **Framework**: Flask 1.1.1
- **Database**: SQLite3
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Migrations**: Flask-Migrate (Alembic)
- **Background Tasks**: Celery
- **Cache**: Redis
- **Containerization**: Docker & Docker Compose
- **Dependency Management**: Poetry


## Quick Start

### Prerequisites

- Python 3.8+
- Poetry
- Postgresql
- Redis
- Docker & Docker Compose (optional)

### Installation

1. **Install dependencies**:
   ```bash
   poetry install
   ```

2. **Set up database**:
   ```bash
   # Run migrations
   poetry run flask db upgrade
   ```

3. **Seed dump data**:
   ```bash
   poetry run python run_seed.py
   ```

4. **Run the application**:
   ```bash
   # Development mode
   poetry run python src/entry.py
   
   # Or using Flask CLI
   FLASK_APP=src.entry:flask_app poetry run flask run  # default port 5000

   # or set port and entry
   export FLASK_RUN_PORT=8080
   export FLASK_APP=src.entry:flask_app
   poetry run flask run
   ```



### Docker for Postgresql & Redis

If you do not have Postgresql & Redis locally, you can use container instead:
1. **Build and run container**
   ```bash
   docker-compose up -d postgres redis
   ```

   After that, run migration and dump data

3. **Access the application**:
   - API: http://localhost:8080/api/
   - Admin: http://localhost:8080/admin/
   - Health Check: http://localhost:8080/

## Configuration

Environment variables:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: Flask secret key for sessions
- `DEV`: Development mode flag
- `FLASK_DEBUG`: Flask debug mode

## Development

### Running Tests
```bash
# Run Flask shell 
FLASK_APP=src.entry:flask_app poetry run flask shell

# Check routes
FLASK_APP=src.entry:flask_app poetry run flask routes
```

### Database Migrations
```bash
# Create migration
poetry run flask db migrate -m "Description"

# Apply migrations
poetry run flask db upgrade

# Check migration status
poetry run flask db show
```

## API document

See API documentation details here: [api_doc.md](./api_doc.md)

