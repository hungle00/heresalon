#!/usr/bin/env python3
"""
Database seeding script for salon management system.
Maps sample data from prepare_data.py to database models.
Skips attributes that don't match DB table fields.
"""

import os
import sys
from decimal import Decimal
from src.entry import flask_app
from src.models import db, Salon, Staff, Service, StaffService, User
from src.models.staff import StaffRole, Seniority
from src.models.service import ServiceType
from src.models.user import UserRole
from werkzeug.security import generate_password_hash

# Import sample data
from prepare_data.data import staffs, services

def create_salon():
    """Create a default salon if it doesn't exist."""
    salon = Salon.query.filter_by(name="Here Salon").first()
    if not salon:
        salon = Salon.create(
            name="Here Salon",
            address="123 Beauty Street, District 1, Ho Chi Minh City"
        )
        print(f"✅ Created salon: {salon.name}")
    else:
        print(f"✅ Salon already exists: {salon.name}")
    return salon

def create_admin_user():
    """Create admin user if it doesn't exist."""
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User.create(
            username="admin",
            email="admin@heresalon.com",
            password_hash=generate_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        print(f"✅ Created admin user: {admin.username}")
    else:
        print(f"✅ Admin user already exists: {admin.username}")
    return admin

def map_staff_data(staff_data, salon_id):
    """Map staff data from prepare_data.py to Staff model fields."""
    # Map seniority string to enum
    seniority_map = {
        'junior': Seniority.JUNIOR,
        'mid': Seniority.MID_LEVEL,
        'senior': Seniority.SENIOR,
        'lead': Seniority.LEAD
    }
    
    # Map role string to StaffRole enum
    role_map = {
        'Senior Nail Artist': StaffRole.STYLIST,
        'Gel Color Specialist': StaffRole.STYLIST,
        'Nail Artist': StaffRole.STYLIST,
        'Spa Pedicure Technician': StaffRole.STYLIST,
        'Acrylic Master': StaffRole.STYLIST,
        'Junior Technician': StaffRole.STYLIST
    }
    
    # Create staff data dict with only matching fields
    staff_dict = {
        'salon_id': salon_id,
        'name': staff_data.get('name'),
        'bio': staff_data.get('bio'),
        'role': role_map.get(staff_data.get('role'), StaffRole.STYLIST).value,
        'years_experience': staff_data.get('years_experience'),
        'seniority': seniority_map.get(staff_data.get('seniority')),
        'rating': staff_data.get('rating'),
        'specialties': ', '.join(staff_data.get('specialties', [])) if staff_data.get('specialties') else None,
        'image_url': staff_data.get('image_url')
    }
    
    # Remove None values
    staff_dict = {k: v for k, v in staff_dict.items() if v is not None}
    
    return staff_dict

def map_service_data(service_data):
    """Map service data from prepare_data.py to Service model fields."""
    # Map category to ServiceType enum
    category_map = {
        'Manicure': ServiceType.NAIL_CARE,
        'Pedicure': ServiceType.NAIL_CARE,
        'Gel': ServiceType.NAIL_CARE,
        'Extensions': ServiceType.NAIL_CARE,
        'Add-on': ServiceType.NAIL_CARE,
        'Spa': ServiceType.NAIL_CARE,
        'Removal': ServiceType.NAIL_CARE,
        'Polish': ServiceType.NAIL_CARE,
        'Kids': ServiceType.NAIL_CARE,
        'Retail': ServiceType.NAIL_CARE
    }
    
    # Create service data dict with only matching fields
    service_dict = {
        'name': service_data.get('name'),
        'description': f"Category: {service_data.get('category', 'Nail Care')}",
        'type': category_map.get(service_data.get('category'), ServiceType.NAIL_CARE),
        'price': Decimal(str(service_data.get('price', 0))) if service_data.get('price') else None,
        'image_url': service_data.get('image_url')
    }
    
    # Remove None values
    service_dict = {k: v for k, v in service_dict.items() if v is not None}
    
    return service_dict

def seed_staffs(salon_id):
    """Seed staff data into database."""
    print("\n🌱 Seeding staff data...")
    
    for staff_data in staffs:
        # Check if staff already exists
        existing_staff = Staff.query.filter_by(name=staff_data['name']).first()
        if existing_staff:
            print(f"⏭️  Staff already exists: {staff_data['name']}")
            continue
        
        # Map data to model fields
        staff_dict = map_staff_data(staff_data, salon_id)
        
        try:
            staff = Staff.create(**staff_dict)
            print(f"✅ Created staff: {staff.name} ({staff.role})")
        except Exception as e:
            print(f"❌ Error creating staff {staff_data['name']}: {e}")

def seed_services():
    """Seed service data into database."""
    print("\n🌱 Seeding service data...")
    
    for service_data in services:
        # Check if service already exists
        existing_service = Service.query.filter_by(name=service_data['name']).first()
        if existing_service:
            print(f"⏭️  Service already exists: {service_data['name']}")
            continue
        
        # Map data to model fields
        service_dict = map_service_data(service_data)
        
        try:
            service = Service.create(**service_dict)
            print(f"✅ Created service: {service.name} (${service.price})")
        except Exception as e:
            print(f"❌ Error creating service {service_data['name']}: {e}")

def create_staff_service_relationships():
    """Create relationships between staff and services based on can_do_services."""
    print("\n🌱 Creating staff-service relationships...")
    
    for staff_data in staffs:
        staff = Staff.query.filter_by(name=staff_data['name']).first()
        if not staff:
            continue
        
        for service_id in staff_data.get('can_do_services', []):
            # Find service by ID from prepare_data.py
            service_data = next((s for s in services if s['id'] == service_id), None)
            if not service_data:
                continue
            
            # Find service in database
            service = Service.query.filter_by(name=service_data['name']).first()
            if not service:
                continue
            
            # Check if relationship already exists
            existing_relationship = StaffService.query.filter_by(
                staff_id=staff.id,
                service_id=service.id
            ).first()
            
            if existing_relationship:
                continue
            
            try:
                StaffService.create(
                    staff_id=staff.id,
                    service_id=service.id
                )
                print(f"✅ Linked {staff.name} to {service.name}")
            except Exception as e:
                print(f"❌ Error linking {staff.name} to {service.name}: {e}")

def main():
    """Main seeding function."""
    print("🚀 Starting database seeding...")
    
    with flask_app.app_context():
        try:
            # Create salon
            salon = create_salon()
            
            # Create admin user
            admin = create_admin_user()
            
            # Seed staff data
            seed_staffs(salon.id)
            
            # Seed service data
            seed_services()
            
            # Create staff-service relationships
            create_staff_service_relationships()
            
            print("\n🎉 Database seeding completed successfully!")
            print(f"📊 Summary:")
            print(f"   - Salons: {Salon.query.count()}")
            print(f"   - Staff: {Staff.query.count()}")
            print(f"   - Services: {Service.query.count()}")
            print(f"   - Staff-Service relationships: {StaffService.query.count()}")
            print(f"   - Users: {User.query.count()}")
            
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
