# Salon Management System

A comprehensive salon management system with React frontend and Flask backend that supports multi-salon operations, staff management, appointment booking, and customer services.

## 🛠 Tech Stack

### **Frontend**
- [React 18](https://github.com/facebook/react) - JavaScript library for building user interfaces
- [React Router DOM](https://github.com/remix-run/react-router) - Client-side routing
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Yarn](https://yarnpkg.com/) - Package manager

### **Backend**
- [Flask 1.1.1](https://github.com/pallets/flask) - Lightweight WSGI web application framework
- [SQLite3](https://www.sqlite.org/) - Lightweight database for development
- [SQLAlchemy](https://github.com/pallets/flask-sqlalchemy) - ORM toolkit
- [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) - Database migrations
- [Celery](https://github.com/celery/celery) - Distributed task queue
- [Redis](https://redis.io/) - In-memory data structure store
- [Poetry](https://python-poetry.org/) - Dependency management

## 🚀 Quick Start

### **Prerequisites**
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- Docker & Docker Compose (optional)
- Yarn (package manager)
- Poetry (Python dependency manager)

### **Option 1: Docker Setup (Recommended)**

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd heresalon
   ```

2. **Start with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Setup Backend**:

   - Access container by this command:
   ```bash
   docker exec -it heresalon-backend-1 bash
   ```
   - After that, run migration and dump data
   ```bash
   poetry run flask db upgrade        # Run database migrations
   poetry run python run_seed.py      # Seed dump data
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8080/api/
   - Admin Interface: http://localhost:8080/admin/

### **Option 2: Manual Setup**

#### **Backend Setup**
```bash
cd backend
poetry install
poetry run flask db upgrade        # Run database migrations
poetry run python run_seed.py      # Seed dump data
FLASK_APP=src.entry:flask_app poetry run flask run --port=8080
```

#### **Frontend Setup**
```bash
cd frontend
yarn install
yarn start
```

## 📚 Documentation

- [Backend Documentation](./backend/README.md) - Detailed Flask backend API and admin interface
- [Frontend Documentation](./frontend/README.md) - React frontend with Tailwind CSS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the [troubleshooting section](#-troubleshooting)
- Review the individual README files in `frontend/` and `backend/`
- Check the console for error messages
- Verify all services are running correctly

**Built with ❤️ for modern salon management**
