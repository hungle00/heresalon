from src.models.base import BaseModel, db


class Salon(BaseModel):
    __tablename__ = 'salons'

    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    staffs = db.relationship('Staff', backref='salon', lazy=True)

    def __repr__(self):
        return f'<Salon {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 