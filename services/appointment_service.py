
from datetime import datetime, timedelta, date

from models.appointment import Appointment
from repositories.appointment_repository import AppointmentRepository
from repositories.service_repository import ServiceRepository
from services.schedule_service import ScheduleService
from exceptions.appointment_errors import InvalidAppointmentError


class AppointmentService:

    def __init__(self):
        self.appointment_repository = AppointmentRepository()
        self.service_repository = ServiceRepository()
        self.schedule_service = ScheduleService()

    def create_booking(
        self,
        user_id,
        service_id,
        appointment_date,
        start_time,
        notes=""
    ):
  
        if appointment_date < date.today():
            raise InvalidAppointmentError(
                "You cannot book an appointment in the past."
            )

        services = self.service_repository.get_all_services()

        selected_service = next(
            (
                item["service"]
                for item in services
                if item["service_id"] == service_id
            ),
            None
        )

        if selected_service is None:
            raise InvalidAppointmentError(
                "The selected service is unavailable."
            )

        start_datetime = datetime.combine(
            appointment_date,
            start_time
        )

        end_datetime = start_datetime + timedelta(
            minutes=selected_service.duration
        )

        end_time = end_datetime.time()

        
        self.schedule_service.validate_business_hours(
            appointment_date,
            start_time,
            end_time
        )

        self.schedule_service.check_slot_availability(
            appointment_date,
            start_time,
            end_time
        )

        appointment = Appointment(
            user_id=user_id,
            service=selected_service,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            notes=notes
        )

        appointment_id = self.appointment_repository.create_appointment(
            appointment,
            service_id
        )

        return appointment_id

    def get_customer_appointments(self, user_id):
        return self.appointment_repository.get_customer_appointments(
            user_id
        )

    def get_all_appointments(self):
        return self.appointment_repository.get_all_appointments()

    def update_appointment_status(
        self,
        appointment_id,
        admin_id,
        new_status
    ):
        allowed_statuses = [
            "approved",
            "rejected",
            "cancelled"
        ]

        if new_status not in allowed_statuses:
            raise InvalidAppointmentError(
                "Invalid appointment status."
            )

        self.appointment_repository.update_status(
            appointment_id,
            admin_id,
            new_status
        )



    def cancel_customer_appointment(self, appointment_id, user_id):
        return self.appointment_repository.cancel_customer_appointment(
            appointment_id,
            user_id
        )