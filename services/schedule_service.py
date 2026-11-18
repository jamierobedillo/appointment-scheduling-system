
from datetime import datetime, timedelta

from repositories.schedule_repository import ScheduleRepository

from exceptions.appointment_errors import (
    InvalidAppointmentError,
    SlotUnavailableError
)


class ScheduleService:

    def __init__(self):
        self.schedule_repository = ScheduleRepository()

    def validate_business_hours(
        self,
        appointment_date,
        start_time,
        end_time
    ):
        # Monday = 1 and Sunday = 7
        day_of_week = appointment_date.isoweekday()

        hours = self.schedule_repository.get_business_hours(
            day_of_week
        )

        if not hours:
            raise InvalidAppointmentError(
                "Business hours have not been configured."
            )

        if hours["is_closed"]:
            raise InvalidAppointmentError(
                "The business is closed on this day."
            )

        opening_time = hours["opening_time"]
        closing_time = hours["closing_time"]

        # Convert MariaDB timedelta values into Python time values.
        if isinstance(opening_time, timedelta):
            opening_time = (
                datetime.min + opening_time
            ).time()

        if isinstance(closing_time, timedelta):
            closing_time = (
                datetime.min + closing_time
            ).time()

        if start_time < opening_time or end_time > closing_time:
            raise InvalidAppointmentError(
                "The selected time is outside business hours."
            )

        return True

    def check_slot_availability(
        self,
        appointment_date,
        start_time,
        end_time
    ):
        conflict = self.schedule_repository.check_slot_conflict(
            appointment_date,
            start_time,
            end_time
        )

        if conflict:
            raise SlotUnavailableError(
                "This appointment time is already taken."
            )

        return True
