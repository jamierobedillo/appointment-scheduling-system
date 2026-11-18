
from datetime import date, time


class Appointment:
    VALID_STATUSES = ["pending", "approved", "rejected", "cancelled"]

    def __init__(
        self,
        user_id,
        service,
        appointment_date,
        start_time,
        end_time,
        notes=""
    ):
        self.user_id = user_id
        self.service = service
        self.appointment_date = appointment_date
        self.start_time = start_time
        self.end_time = end_time
        self.notes = notes
        self.status = "pending"

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Invalid customer ID.")

        self.__user_id = value

    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, value):
        if value is None:
            raise ValueError("Please select a service.")

        self.__service = value

    @property
    def appointment_date(self):
        return self.__appointment_date

    @appointment_date.setter
    def appointment_date(self, value):
        if not isinstance(value, date):
            raise ValueError("Invalid appointment date.")

        self.__appointment_date = value

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        if not isinstance(value, time):
            raise ValueError("Invalid start time.")

        self.__start_time = value

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, value):
        if not isinstance(value, time) or value <= self.start_time:
            raise ValueError("End time must be later than start time.")

        self.__end_time = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError("Invalid appointment status.")

        self.__status = value

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, value):
        self.__notes = value or ""
