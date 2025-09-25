#!/usr/bin/env python3
"""
Script to create default admin user
"""
import sys
import os

# Add src path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from werkzeug.security import generate_password_hash
from src.models import db, User
from src.models.user import UserRole
from src.settings import Settings

def create_admin():
    """Create default admin user"""
    # Initialize Flask app
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object(Settings)
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Create tables if not exist
        db.create_all()
        
        # Check if admin already exists
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print("Admin user already exists!")
            return
        
        # Create default admin user
        admin_user = User(
            username='admin',
            email='admin@salon.com',
            password_hash=generate_password_hash('admin123'),
            role=UserRole.ADMIN
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@salon.com")

if __name__ == '__main__':
    create_admin()
