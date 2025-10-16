from enum import Enum
from datetime import datetime
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
import re
from src.models.base import BaseModel, db


class AppointmentStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Appointment(BaseModel):
    __tablename__ = 'appointments'

    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    # Constraint to ensure either user_id or phone_number is present
    __table_args__ = (
        CheckConstraint(
            '(user_id IS NOT NULL) OR (phone_number IS NOT NULL)',
            name='check_user_or_phone'
        ),
    )

    # Relationships
    user = db.relationship('User', backref='appointments', lazy=True)

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        """Validate phone number format"""
        if phone_number is None:
            return phone_number
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', phone_number)
        
        # Check if it has 10-15 digits (common phone number lengths)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must have 10-15 digits')
        
        # Check if it contains only digits and common phone characters
        phone_pattern = r'^[\+]?[0-9\s\-\(\)]{10,20}$'
        if not re.match(phone_pattern, phone_number):
            raise ValueError('Invalid phone number format')
        
        return phone_number

    @validates('date')
    def validate_date(self, key, date):
        """Validate appointment date"""
        if date is None:
            raise ValueError('Date is required')
        
        # Check if date is not in the past
        if date < datetime.now().date():
            raise ValueError('Appointment date cannot be in the past')
        
        return date

    @validates('start_time', 'end_time')
    def validate_times(self, key, time_value):
        """Validate start_time and end_time"""
        if time_value is None:
            raise ValueError(f'{key} is required')
        
        return time_value

    def __repr__(self):
        return f'<Appointment {self.id} - {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'user_id': self.user_id,
            'service_id': self.service_id,
            'phone_number': self.phone_number,
            'status': self.status.value,
            'date': self.date.isoformat() if self.date else None,
            'start_time': self.start_time.time().strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.time().strftime('%H:%M') if self.end_time else None
        } 
