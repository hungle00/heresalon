from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy import and_, or_
from src.models import db, Appointment, Staff, WorkingHour
from src.models.appointment import AppointmentStatus


class AvailabilityService:
    """Service class for handling appointment availability logic.
    from src.services.availability_service import AvailabilityService
    """
    
    @staticmethod
    def check_staff_availability(
        staff_id: int,
        appointment_date: date,
        start_time: datetime,
        end_time: datetime,
        exclude_appointment_id: Optional[int] = None
    ) -> Dict:
        """
        Check if a staff member is available for a given time slot.
        
        Args:
            staff_id: ID of the staff member
            appointment_date: Date of the appointment
            start_time: Start time of the appointment
            end_time: End time of the appointment
            exclude_appointment_id: ID of appointment to exclude (for editing)
            
        Returns:
            Dict with availability status and conflicts
        """
        # Check for time conflicts
        query = Appointment.query.filter(
            and_(
                Appointment.staff_id == staff_id,
                Appointment.date == appointment_date,
                Appointment.status != AppointmentStatus.CANCELLED,
                or_(
                    and_(Appointment.start_time <= start_time, Appointment.end_time > start_time),
                    and_(Appointment.start_time < end_time, Appointment.end_time >= end_time),
                    and_(Appointment.start_time >= start_time, Appointment.end_time <= end_time)
                )
            )
        )
        
        if exclude_appointment_id:
            query = query.filter(Appointment.id != exclude_appointment_id)
        
        conflicts = query.all()
        
        return {
            'available': len(conflicts) == 0,
            'conflicts': [{
                'id': conflict.id,
                'start_time': conflict.start_time.isoformat(),
                'end_time': conflict.end_time.isoformat(),
                'service': conflict.service.name if conflict.service else None,
                'customer': conflict.user.username if conflict.user else None,
                'status': conflict.status.value
            } for conflict in conflicts]
        }
    
    @staticmethod
    def get_staff_working_hours(staff_id: int, appointment_date: date) -> List[Dict]:
        """
        Get working hours for a staff member on a specific date.
        
        Args:
            staff_id: ID of the staff member
            appointment_date: Date to check
            
        Returns:
            List of working hour periods
        """
        # Get day of week (0 = Monday, 6 = Sunday)
        day_of_week = appointment_date.weekday()
        
        working_hours = WorkingHour.query.filter(
            and_(
                WorkingHour.staff_id == staff_id,
                WorkingHour.day_of_week == day_of_week
            )
        ).all()
        
        return [{
            'start_time': wh.start_time.strftime('%H:%M'),
            'end_time': wh.end_time.strftime('%H:%M'),
            'is_available': wh.is_available
        } for wh in working_hours]
    
    @staticmethod
    def get_available_time_slots(
        staff_id: int,
        appointment_date: date,
        service_duration_minutes: int = 60,
        slot_interval_minutes: int = 30
    ) -> List[Dict]:
        # TODO: 
        raise NotImplementedError

