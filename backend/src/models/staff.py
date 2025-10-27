from enum import Enum
from src.models.base import BaseModel, db


class StaffRole(Enum):
    STYLIST = 1
    MANAGER = 2
    RECEPTIONIST = 3


class Seniority(Enum):
    JUNIOR = "junior"
    MID_LEVEL = "mid_level"
    SENIOR = "senior"
    LEAD = "lead"


class Staff(BaseModel):
    __tablename__ = 'staffs'

    salon_id = db.Column(db.Integer, db.ForeignKey('salons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Optional user account
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    role = db.Column(db.Integer, nullable=False)  # Staff role as integer
    years_experience = db.Column(db.Integer, nullable=True)
    seniority = db.Column(db.Enum(Seniority), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    specialties = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    user = db.relationship('User', backref='staff_profile', lazy=True)
    appointments = db.relationship('Appointment', backref='staff', lazy=True)
    # working_hours = db.relationship('WorkingHour', backref='staff', lazy=True)

    def __repr__(self):
        return f'<Staff {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'salon_id': self.salon_id,
            'user_id': self.user_id,
            'name': self.name,
            'bio': self.bio,
            'role': self.role,
            'years_experience': self.years_experience,
            'seniority': self.seniority.value if self.seniority else None,
            'rating': self.rating,
            'specialties': self.specialties,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
