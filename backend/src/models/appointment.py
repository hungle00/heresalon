from enum import Enum
from datetime import datetime
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    # Relationships
    user = db.relationship('User', backref='appointments', lazy=True)

    def __repr__(self):
        return f'<Appointment {self.id} - {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'user_id': self.user_id,
            'service_id': self.service_id,
            'status': self.status.value,
            'date': self.date.isoformat() if self.date else None,
            'start_time': self.start_time.time().strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.time().strftime('%H:%M') if self.end_time else None
        } 
