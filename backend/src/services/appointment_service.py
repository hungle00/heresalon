from datetime import datetime, date, time
import re
from typing import Optional, List, Dict, Any, Tuple
from flask import current_app

from src.models import Appointment, Staff, Service, User
from src.models.appointment import AppointmentStatus
from src.settings import Settings  
from twilio.rest import Client

class AppointmentService:
    """Service class for appointment operations that can be reused across API and chatbot"""
    
    @staticmethod
    def _validate_time_format(time_str: str) -> bool:
        """Validate time format (HH:MM)"""
        time_pattern = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
        return re.match(time_pattern, time_str) is not None
    
    @staticmethod
    def _parse_appointment_data(data: Dict[str, Any], user_id: Optional[int] = None) -> Tuple[Dict[str, Any], Optional[str]]:
        """
        Parse and validate appointment data
        
        Args:
            data: Raw appointment data
            user_id: Optional user ID for authenticated users
            
        Returns:
            Tuple of (parsed_data, error_message)
        """
        try:
            # Determine required fields based on authentication status
            if user_id:
                # Authenticated user
                required_fields = ['staff_id', 'service_id', 'date', 'start_time', 'end_time']
                phone_number = None
            else:
                # Guest user - phone_number is required
                required_fields = ['staff_id', 'service_id', 'date', 'start_time', 'end_time', 'customer_phone']
                
                if 'customer_phone' not in data:
                    return None, 'Phone number is required for guest booking'
                phone_number = data['customer_phone']
            
            # Check required fields
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return None, f'Missing required fields: {", ".join(missing_fields)}'
            
            # Parse date
            try:
                appointment_date = date.fromisoformat(data['date'])
            except ValueError:
                return None, 'Invalid date format. Use YYYY-MM-DD'
            
            # Parse and validate time strings
            start_time_str = data['start_time']
            end_time_str = data['end_time']
            
            if not AppointmentService._validate_time_format(start_time_str):
                return None, 'Invalid start_time format. Use HH:MM (e.g., 10:00)'
                
            if not AppointmentService._validate_time_format(end_time_str):
                return None, 'Invalid end_time format. Use HH:MM (e.g., 11:30)'
            
            # Parse time strings to time objects
            start_time_obj = time.fromisoformat(start_time_str)
            end_time_obj = time.fromisoformat(end_time_str)
            
            # Validate that start_time is earlier than end_time
            if start_time_obj >= end_time_obj:
                return None, 'start_time must be earlier than end_time'
            
            # Combine date and time to create datetime objects
            start_datetime = datetime.combine(appointment_date, start_time_obj)
            end_datetime = datetime.combine(appointment_date, end_time_obj)
            
            # Validate that appointment is not in the past
            if start_datetime < datetime.now():
                return None, 'Cannot create appointment in the past'
            
            # Check if staff exists
            staff = Staff.get(id=data['staff_id'])
            if not staff:
                return None, 'Staff member not found'
            
            # Check if service exists
            service = Service.get(id=data['service_id'])
            if not service:
                return None, 'Service not found'
            
            # Check if staff and service belong to same salon
            if staff.salon_id != service.salon_id:
                return None, 'Staff and service must belong to the same salon'
            
            # Check for time conflicts
            conflict = AppointmentService.check_time_conflict(
                staff_id=data['staff_id'],
                start_time=start_datetime,
                end_time=end_datetime,
                exclude_appointment_id=None
            )
            if conflict:
                return None, f'Time conflict: {conflict}'
            
            parsed_data = {
                'staff_id': data['staff_id'],
                'user_id': user_id,
                'service_id': data['service_id'],
                'phone_number': phone_number,
                'status': AppointmentStatus(data.get('status', 'pending')),
                'date': appointment_date,
                'start_time': start_datetime,
                'end_time': end_datetime
            }
            
            return parsed_data, None
            
        except Exception as e:
            return None, f'Data validation error: {str(e)}'
    
    @staticmethod
    def create_appointment(data: Dict[str, Any], user_id: Optional[int] = None) -> Tuple[Optional[Appointment], Optional[str]]:
        """
        Create a new appointment
        
        Args:
            data: Appointment data
            user_id: Optional user ID for authenticated users
            
        Returns:
            Tuple of (appointment, error_message)
        """
        try:
            # Parse and validate data
            parsed_data, error = AppointmentService._parse_appointment_data(data, user_id)
            if error:
                return None, error
            
            # Create appointment
            appointment = Appointment.create(**parsed_data)
            return appointment, None
            
        except Exception as e:
            return None, f'Failed to create appointment: {str(e)}'
    
    @staticmethod
    def get_appointments(user_id: int) -> List[Appointment]:
        """
        Get appointments for a specific user
        
        Args:
            user_id: User ID to get appointments for
            
        Returns:
            List of appointments
        """
        try:
            query = Appointment.query.filter_by(user_id=user_id)
            return query.order_by(Appointment.start_time.desc()).all()
            
        except Exception as e:
            current_app.logger.error(f'Error getting appointments: {str(e)}')
            return []
    
    @staticmethod
    def get_appointment_by_id(appointment_id: int, user_id: Optional[int] = None) -> Tuple[Optional[Appointment], Optional[str]]:
        """
        Get appointment by ID with access control
        
        Args:
            appointment_id: Appointment ID
            user_id: User ID for access control
            
        Returns:
            Tuple of (appointment, error_message)
        """
        try:
            appointment = Appointment.get(id=appointment_id)
            if not appointment:
                return None, 'Appointment not found'
            
            # Check access permissions - only allow access to own appointments
            if user_id and appointment.user_id != user_id:
                return None, 'Access denied'
            
            return appointment, None
            
        except Exception as e:
            return None, f'Error getting appointment: {str(e)}'
    
    @staticmethod
    def update_appointment(appointment_id: int, data: Dict[str, Any], 
                          user_id: Optional[int] = None) -> Tuple[Optional[Appointment], Optional[str]]:
        """
        Update appointment with access control
        
        Args:
            appointment_id: Appointment ID
            data: Update data
            user_id: User ID for access control
            
        Returns:
            Tuple of (appointment, error_message)
        """
        try:
            appointment, error = AppointmentService.get_appointment_by_id(appointment_id, user_id)
            if error:
                return None, error
            
            # Update fields
            if 'status' in data:
                try:
                    appointment.status = AppointmentStatus(data['status'])
                except ValueError:
                    return None, 'Invalid status value'
            
            if 'date' in data:
                try:
                    appointment.date = date.fromisoformat(data['date'])
                except ValueError:
                    return None, 'Invalid date format. Use YYYY-MM-DD'
            
            if 'start_time' in data:
                start_time_str = data['start_time']
                if not AppointmentService._validate_time_format(start_time_str):
                    return None, 'Invalid start_time format. Use HH:MM (e.g., 10:00)'
                
                start_time_obj = time.fromisoformat(start_time_str)
                start_datetime = datetime.combine(appointment.date, start_time_obj)
                appointment.start_time = start_datetime
            
            if 'end_time' in data:
                end_time_str = data['end_time']
                if not AppointmentService._validate_time_format(end_time_str):
                    return None, 'Invalid end_time format. Use HH:MM (e.g., 11:30)'
                
                end_time_obj = time.fromisoformat(end_time_str)
                end_datetime = datetime.combine(appointment.date, end_time_obj)
                appointment.end_time = end_datetime
            
            # Validate that start_time is earlier than end_time
            if appointment.start_time >= appointment.end_time:
                return None, 'start_time must be earlier than end_time'
            
            # Check for time conflicts (excluding current appointment)
            conflict = AppointmentService.check_time_conflict(
                staff_id=appointment.staff_id,
                start_time=appointment.start_time,
                end_time=appointment.end_time,
                exclude_appointment_id=appointment_id
            )
            if conflict:
                return None, f'Time conflict: {conflict}'
            
            appointment.save()
            return appointment, None
            
        except Exception as e:
            return None, f'Error updating appointment: {str(e)}'
    
    @staticmethod
    def delete_appointment(appointment_id: int, user_id: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Delete appointment with access control
        
        Args:
            appointment_id: Appointment ID
            user_id: User ID for access control
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            appointment, error = AppointmentService.get_appointment_by_id(appointment_id, user_id)
            if error:
                return False, error
            
            appointment.delete()
            return True, None
            
        except Exception as e:
            return False, f'Error deleting appointment: {str(e)}'
    
    @staticmethod
    def check_time_conflict(staff_id: int, start_time: datetime, end_time: datetime, 
                           exclude_appointment_id: Optional[int] = None) -> Optional[str]:
        """
        Check for time conflicts with existing appointments
        
        Args:
            staff_id: Staff ID
            start_time: Start time
            end_time: End time
            exclude_appointment_id: Appointment ID to exclude from conflict check
            
        Returns:
            Conflict message if found, None otherwise
        """
        try:
            # Find overlapping appointments
            query = Appointment.query.filter_by(staff_id=staff_id).filter(
                Appointment.start_time < end_time,
                Appointment.end_time > start_time
            )
            
            if exclude_appointment_id:
                query = query.filter(Appointment.id != exclude_appointment_id)
            
            conflicting_appointments = query.all()
            
            if conflicting_appointments:
                conflict_info = []
                for apt in conflicting_appointments:
                    conflict_info.append(f"Appointment #{apt.id} ({apt.start_time.strftime('%H:%M')}-{apt.end_time.strftime('%H:%M')})")
                
                return f"Staff has conflicting appointments: {', '.join(conflict_info)}"
            
            return None
            
        except Exception as e:
            return f"Error checking time conflicts: {str(e)}"

    @staticmethod
    def _lookup_phone(user_id: Optional[int], fallback: Optional[str] = None) -> Optional[str]:
        """Resolve phone number via explicit fallback or User model."""
        if fallback:
            return fallback
        if user_id:
            try:
                user = User.get(id=user_id)
                if user and getattr(user, "phone_number", None):
                    return user.phone_number  # type: ignore[attr-defined]
            except Exception as e:
                current_app.logger.warning(f"Phone lookup failed: {e}")
        return None

    @staticmethod
    def _format_time(dt: Optional[datetime]) -> str:
        try:
            return dt.strftime("%H:%M") if dt else ""
        except Exception:
            return ""

    @staticmethod
    def build_confirmation_message(action: str, appt: Appointment) -> str:
        """
        Build a short, consistent confirmation message for SMS across create/update/delete.
        """
        # Use Appointment fields safely
        appt_date = getattr(appt, "date", None)
        appt_start = getattr(appt, "start_time", None)
        appt_end = getattr(appt, "end_time", None)

        date_str = appt_date.isoformat() if isinstance(appt_date, date) else ""
        start_str = AppointmentService._format_time(appt_start)
        end_str = AppointmentService._format_time(appt_end)

        if action == "deleted":
            return f"Your HereSalon appointment on {date_str} ({start_str}-{end_str}) has been canceled. If this is unexpected, reply or call us."
        elif action == "updated":
            return f"Your HereSalon appointment was updated: {date_str} from {start_str} to {end_str}. See you soon!"
        else:  # created / default
            return f"Your HereSalon appointment is confirmed for {date_str} from {start_str} to {end_str}. We look forward to seeing you!"

    @staticmethod
    def send_message(phone_number: str, body: str) -> bool:
        """
        Generic Twilio SMS sender. Returns True on success, False otherwise.
        Safe to call even if Twilio is not configured.
        """
        if not phone_number:
            current_app.logger.info("No phone number provided; skipping SMS.")
            return False

        if not (Settings.TWILIO_ACCOUNT_SID and Settings.TWILIO_AUTH_TOKEN and Settings.TWILIO_PHONE_NUMBER):
            current_app.logger.warning("Twilio credentials are missing; skipping SMS confirmation.")
            return False

        if Client is None:
            current_app.logger.warning("twilio SDK not installed; skipping SMS confirmation.")
            return False

        try:
            twilio_client = Client(Settings.TWILIO_ACCOUNT_SID, Settings.TWILIO_AUTH_TOKEN)
            twilio_client.messages.create(
                body=body,
                from_=Settings.TWILIO_PHONE_NUMBER,
                to=phone_number,
            )
            return True
        except Exception as sms_err:
            current_app.logger.error(f"Twilio SMS sending failed: {sms_err}")
            return False

    @staticmethod
    def send_confirmation(appointment: Appointment, action: str,
                          user_id: Optional[int] = None,
                          customer_phone: Optional[str] = None) -> None:
        """
        Resolve phone, build message for action ('created'|'updated'|'deleted'), and send it.
        """
        try:
            phone = AppointmentService._lookup_phone(user_id, customer_phone) or getattr(appointment, "phone_number", None)
            body = AppointmentService.build_confirmation_message(action, appointment)
            AppointmentService.send_message(phone or "", body)
        except Exception as e:
            current_app.logger.error(f"Error while sending confirmation SMS: {e}")