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
from src.models import db, Salon, Staff, Service, User, Appointment
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
            address="123 Beauty Street, District 1, Ho Chi Minh City",
            description="Premium nail salon offering professional nail care services including manicures, pedicures, gel polish, nail art, and spa treatments. Our experienced staff provides exceptional service in a relaxing environment."
        )
        print(f"✅ Created salon: {salon.name}")
    else:
        print(f"✅ Salon already exists: {salon.name}")
    return salon

def create_admin():
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

def create_manager(salon_id):
    """Create manager user if it doesn't exist."""
    manager = User.query.filter_by(username="manager").first()
    if not manager:
        manager = User.create(
            username="manager",
            email="manager@heresalon.com",
            password_hash=generate_password_hash("manager123"),
            role=UserRole.MANAGER,
            salon_id=salon_id
        )
        print(f"✅ Created manager user: {manager.username} for salon ID: {salon_id}")
    else:
        print(f"✅ Manager user already exists: {manager.username}")
    return manager

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
    
    salon = Salon.query.first()
    # Create service data dict with only matching fields
    service_dict = {
        'name': service_data.get('name'),
        'description': f"Category: {service_data.get('category', 'Nail Care')}",
        'type': category_map.get(service_data.get('category'), ServiceType.NAIL_CARE),
        'price': Decimal(str(service_data.get('price', 0))) if service_data.get('price') else None,
        'image_url': service_data.get('image_url'),
        'salon_id': salon.id
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

def create_appointment_data():
    """Create appointment data for October 2025 with 30-minute time slots."""
    print("\n🌱 Creating appointment data for October 2025...")
    
    from datetime import datetime, date, time, timedelta
    from src.models.appointment import Appointment, AppointmentStatus
    
    # Get existing staff and services
    staffs = Staff.query.all()
    services = Service.query.all()
    users = User.query.filter(User.role.in_([UserRole.ADMIN, UserRole.MANAGER])).all()
    
    if not staffs or not services or not users:
        print("❌ Need staff, services, and users to create appointments")
        return

    # October 2025 dates
    october_2025 = date(2025, 11, 1)
    
    # Time slots (30-minute intervals from 9:00 AM to 6:00 PM)
    time_slots = [
        time(9, 0),   # 9:00 AM
        time(9, 30),  # 9:30 AM
        time(10, 0),  # 10:00 AM
        time(10, 30), # 10:30 AM
        time(11, 0),  # 11:00 AM
        time(11, 30), # 11:30 AM
        time(12, 0),  # 12:00 PM
        time(12, 30), # 12:30 PM
        time(13, 0),  # 1:00 PM
        time(13, 30), # 1:30 PM
        time(14, 0),  # 2:00 PM
        time(14, 30), # 2:30 PM
        time(15, 0),  # 3:00 PM
        time(15, 30), # 3:30 PM
        time(16, 0),  # 4:00 PM
        time(16, 30), # 4:30 PM
        time(17, 0),  # 5:00 PM
        time(17, 30), # 5:30 PM
        time(18, 0),  # 6:00 PM
    ]
    # Status options
    statuses = [AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED, AppointmentStatus.COMPLETED]
    
    # Create appointments for the first 15 days of October 2025
    appointments_created = 0

    for day in range(1, 10):  # October 1-15, 2025
        appointment_date = date(2025, 11, day)
        
        # Skip weekends (Saturday = 5, Sunday = 6)
        if appointment_date.weekday() >= 5:
            continue
            
        # Create 2-4 appointments per day
        num_appointments = 2 + (day % 3)  # 2, 3, or 4 appointments

        for i in range(num_appointments):
            # Randomly select staff, service, and user
            import random
            staff = random.choice(staffs)
            service = random.choice(services)
            user = random.choice(users)
            
            # Select a random time slot
            start_time_slot = random.choice(time_slots[:-1])  # Don't pick the last slot
            start_datetime = datetime.combine(appointment_date, start_time_slot)
            end_datetime = start_datetime + timedelta(minutes=30)

            # Check if appointment already exists
            existing = Appointment.query.filter_by(
                staff_id=staff.id,
                date=appointment_date,
                start_time=start_datetime
            ).first()
            
            if existing:
                continue

            try:
                appointment = Appointment.create(
                    staff_id=staff.id,
                    user_id=user.id,
                    service_id=service.id,
                    status=random.choice(statuses),
                    date=appointment_date,
                    start_time=start_datetime,
                    end_time=end_datetime
                )
                appointments_created += 1
                print(f"✅ Created appointment: {appointment_date} {start_time_slot} - {staff.name} & {service.name}")
                
            except Exception as e:
                print(f"❌ Error creating appointment: {e}")
    
    print(f"🎉 Created {appointments_created} appointments for October 2025!")

def main():
    """Main seeding function."""
    print("🚀 Starting database seeding...")
    
    with flask_app.app_context():
        try:
            # Create salon
            salon = create_salon()
            
            # Create admin user
            admin = create_admin()
            
            # Create manager user for the salon
            manager = create_manager(salon.id)
            
            # Seed staff data
            seed_staffs(salon.id)
            
            # Seed service data
            seed_services()

            # Create appointment data
            create_appointment_data()
            
            print("\n🎉 Database seeding completed successfully!")
            print(f"📊 Summary:")
            print(f"   - Salons: {Salon.query.count()}")
            print(f"   - Staff: {Staff.query.count()}")
            print(f"   - Services: {Service.query.count()}")
            print(f"   - Users: {User.query.count()}")
            print(f"   - Admin users: {User.query.filter_by(role=UserRole.ADMIN).count()}")
            print(f"   - Manager users: {User.query.filter_by(role=UserRole.MANAGER).count()}")
            print(f"   - Appointments: {Appointment.query.count()}")
            
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
