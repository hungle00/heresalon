from src.models.base import BaseModel, db


class StaffService(BaseModel):
    __tablename__ = 'staff_services'

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)

    # Unique constraint
    __table_args__ = (db.UniqueConstraint('service_id', 'staff_id', name='unique_staff_service'),)

    def __repr__(self):
        return f'<StaffService staff_id={self.staff_id} service_id={self.service_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'service_id': self.service_id,
            'staff_id': self.staff_id
        } 