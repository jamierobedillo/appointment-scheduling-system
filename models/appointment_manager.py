
from models.appointment import Appointment


class AppointmentManager:

    def __init__(self):
        self.__appointments = []

    def add_appointment(self, appointment):
        if not isinstance(appointment, Appointment):
            raise TypeError("Only Appointment objects can be added.")

        if appointment.appointment_id is None:
            existing_ids = [
                item.appointment_id or 0
                for item in self.__appointments
            ]

            appointment.appointment_id = max(existing_ids, default=0) + 1

        self.__appointments.append(appointment)

    def get_all_appointments(self):
        return self.__appointments.copy()

    def find_appointment(self, appointment_id):
        for appointment in self.__appointments:
            if appointment.appointment_id == appointment_id:
                return appointment

        return None

    def cancel_appointment(self, appointment):
        if appointment not in self.__appointments:
            raise ValueError("Appointment does not exist.")

        if appointment.status in ["rejected", "cancelled"]:
            raise ValueError("This appointment cannot be cancelled.")

        appointment.status = "cancelled"
        return True

    def get_appointment_count(self):
        return len(self.__appointments)
