from enum import Enum
from src.models.base import BaseModel, db
from sqlalchemy import CheckConstraint


class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"

class User(BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    # Add salon_id for managers to know which salon they manage
    salon_id = db.Column(db.Integer, db.ForeignKey('salons.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    managed_salon = db.relationship('Salon', foreign_keys=[salon_id], backref='managers')
    
    # Validation: Only MANAGER role can have salon_id
    __table_args__ = (
        CheckConstraint(
            "(role = 'manager' AND salon_id IS NOT NULL) OR (role != 'manager' AND salon_id IS NULL)",
            name='check_manager_has_salon'
        ),
    )

    def __repr__(self):
        return f'<User {self.username} ({self.role.value})>'

    @property
    def is_customer(self):
        return self.role == UserRole.CUSTOMER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_manager(self):
        return self.role == UserRole.MANAGER

    @property
    def is_staff(self):
        return self.role == UserRole.STAFF

    def validate_salon_assignment(self):
        """Validate that only managers can have salon_id"""
        if self.role == UserRole.MANAGER and self.salon_id is None:
            raise ValueError("Manager must be assigned to a salon")
        if self.role != UserRole.MANAGER and self.salon_id is not None:
            raise ValueError("Only managers can be assigned to a salon")
        return True

    def save(self):
        """Override save to include validation"""
        self.validate_salon_assignment()
        return super().save()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'salon_id': self.salon_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
