from enum import Enum
from src.models.base import BaseModel, db


class DayOfWeek(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class WorkingHour(BaseModel):
    __tablename__ = 'working_hours'

    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<WorkingHour {self.staff_id} - {self.day_of_week.value}>'

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'staff_id': self.staff_id,
            'day_of_week': self.day_of_week.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        } 