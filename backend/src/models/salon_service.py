from src.models.base import BaseModel, db


class SalonService(BaseModel):
    __tablename__ = 'salon_services'

    salon_id = db.Column(db.Integer, db.ForeignKey('salons.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    # Unique constraint to prevent duplicate salon-service pairs
    __table_args__ = (db.UniqueConstraint('salon_id', 'service_id', name='unique_salon_service'),)

    def __repr__(self):
        return f'<SalonService salon_id={self.salon_id} service_id={self.service_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'salon_id': self.salon_id,
            'service_id': self.service_id
        }
