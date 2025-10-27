from src.models.base import BaseModel, db


class Salon(BaseModel):
    __tablename__ = 'salons'

    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)  # Add description field
    uuid = db.Column(db.String(36), nullable=True)  # Add uuid field
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    start_working_time = db.Column(db.Time, nullable=True)
    end_working_time = db.Column(db.Time, nullable=True)

    # Relationships
    staffs = db.relationship('Staff', backref='salon', lazy=True)
    services = db.relationship('Service', backref='salon', lazy=True)

    def __repr__(self):
        return f'<Salon {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'address': self.address,
            'description': self.description,
            'start_working_time': self.start_working_time.isoformat() if self.start_working_time else None,
            'end_working_time': self.end_working_time.isoformat() if self.end_working_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'staff_count': len(self.staffs) if self.staffs else 0,
            'services_count': len(self.services) if self.services else 0
        }
