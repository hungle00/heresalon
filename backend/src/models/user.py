from enum import Enum
from src.models.base import BaseModel, db


class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username} ({self.role.value})>'

    @property
    def is_customer(self):
        return self.role == UserRole.CUSTOMER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 