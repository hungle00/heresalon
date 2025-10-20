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

    salon_id = db.Column(db.Integer, db.ForeignKey('salons.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.Enum(ServiceType), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # Duration in minutes
    image_url = db.Column(db.String(255), nullable=True)

    # Relationships
    appointments = db.relationship('Appointment', backref='service', lazy=True)

    def __repr__(self):
        return f'<Service {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'salon_id': self.salon_id,
            'name': self.name,
            'description': self.description,
            'type': self.type.value,
            'price': float(self.price) if self.price else None,
            'duration': self.duration,
            'image_url': self.image_url
        }
