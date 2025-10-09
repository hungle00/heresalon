from enum import Enum
from decimal import Decimal
from src.models.base import BaseModel, db


class ServiceType(Enum):
    HAIR_CUT = "hair_cut"
    HAIR_COLOR = "hair_color"
    HAIR_STYLING = "hair_styling"
    NAIL_CARE = "nail_care"
    FACIAL = "facial"
    MASSAGE = "massage"


class Service(BaseModel):
    __tablename__ = 'services'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.Enum(ServiceType), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)

    # Relationships
    salon_services = db.relationship('SalonService', backref='service', lazy=True)
    appointments = db.relationship('Appointment', backref='service', lazy=True)

    def __repr__(self):
        return f'<Service {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type.value,
            'price': float(self.price) if self.price else None,
            'image_url': self.image_url
        }
