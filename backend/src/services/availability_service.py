from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy import and_, or_
from src.models import db, Appointment, Staff
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
    ) -> bool:
        """
        Check if a staff member is available for a given time slot.
        
        Args:
            staff_id: ID of the staff member
            appointment_date: Date of the appointment
            start_time: Start time of the appointment
            end_time: End time of the appointment
            exclude_appointment_id: ID of appointment to exclude (for editing)
            
        Returns:
            bool: True if available, False if conflicts exist
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
        
        conflicts_count = query.count()
        return conflicts_count == 0
    
    @staticmethod
    def get_available_time_slots(
        staff_id: int,
        appointment_date: date,
        service_duration_minutes: int = 60,
        slot_interval_minutes: int = 30
    ) -> List[str]:
        """
        Get available time slots for a staff member on a specific date.
        
        Args:
            staff_id: ID of the staff member
            appointment_date: Date to check availability
            service_duration_minutes: Duration of the service in minutes
            slot_interval_minutes: Interval between time slots in minutes
            
        Returns:
            List of available time slots in HH:MM format
        """
        # Get staff information and salon working hours
        staff = Staff.query.get(staff_id)
        if not staff:
            return []
        
        salon = staff.salon
        if not salon or not salon.start_working_time or not salon.end_working_time:
            return []
        
        # Convert salon working hours to datetime for the appointment date
        start_working_time = datetime.combine(appointment_date, salon.start_working_time)
        end_working_time = datetime.combine(appointment_date, salon.end_working_time)
        
        # Generate all possible time slots
        available_slots = []
        current_time = start_working_time
        
        while current_time + timedelta(minutes=service_duration_minutes) <= end_working_time:
            slot_start = current_time
            slot_end = current_time + timedelta(minutes=service_duration_minutes)
            
            # Check if this slot conflicts with existing appointments
            is_available = AvailabilityService.check_staff_availability(
                staff_id=staff_id,
                appointment_date=appointment_date,
                start_time=slot_start,
                end_time=slot_end
            )
            
            # If no conflicts, add to available slots
            if is_available:
                available_slots.append(slot_start.strftime('%H:%M'))
            
            # Move to next slot
            current_time += timedelta(minutes=slot_interval_minutes)
        
        return available_slots

