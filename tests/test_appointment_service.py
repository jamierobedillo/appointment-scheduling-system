
import unittest
from unittest.mock import MagicMock, patch
from datetime import date, time

from services.appointment_service import AppointmentService
from models.service import Service
from exceptions.appointment_errors import InvalidAppointmentError


class TestAppointmentService(unittest.TestCase):

    def setUp(self):
        self.appointment_service = AppointmentService()

        self.appointment_service.appointment_repository = MagicMock()
        self.appointment_service.service_repository = MagicMock()
        self.appointment_service.schedule_service = MagicMock()

        self.sample_service = Service(
            "General Consultation",
            "General consultation",
            30,
            500
        )

        self.appointment_service.service_repository.get_all_services.return_value = [
            {
                "service_id": 1,
                "service": self.sample_service
            }
        ]

    def test_create_booking_successfully(self):
        self.appointment_service.appointment_repository.create_appointment.return_value = 1

        appointment_id = self.appointment_service.create_booking(
            1,
            1,
            date(2026, 11, 21),
            time(10, 0),
            "Test booking"
        )

        self.assertEqual(appointment_id, 1)
        self.appointment_service.appointment_repository.create_appointment.assert_called_once()

    def test_booking_rejects_past_date(self):
        with patch("services.appointment_service.date") as mock_date:
            mock_date.today.return_value = date(2026, 11, 18)

            with self.assertRaises(InvalidAppointmentError):
                self.appointment_service.create_booking(
                    1,
                    1,
                    date(2026, 11, 17),
                    time(10, 0)
                )

    def test_booking_rejects_unavailable_service(self):
        with self.assertRaises(InvalidAppointmentError):
            self.appointment_service.create_booking(
                1,
                99,
                date(2026, 11, 21),
                time(10, 0)
            )

    def test_booking_checks_business_hours(self):
        self.appointment_service.create_booking(
            1,
            1,
            date(2026, 11, 21),
            time(10, 0)
        )

        self.appointment_service.schedule_service.validate_business_hours.assert_called_once()

    def test_booking_checks_slot_availability(self):
        self.appointment_service.create_booking(
            1,
            1,
            date(2026, 11, 21),
            time(10, 0)
        )

        self.appointment_service.schedule_service.check_slot_availability.assert_called_once()

    def test_get_customer_appointments(self):
        expected_appointments = [
            {"appointment_id": 1, "status": "pending"}
        ]

        self.appointment_service.appointment_repository.get_customer_appointments.return_value = expected_appointments

        result = self.appointment_service.get_customer_appointments(1)

        self.assertEqual(result, expected_appointments)

    def test_get_all_appointments(self):
        expected_appointments = [
            {"appointment_id": 1, "status": "approved"}
        ]

        self.appointment_service.appointment_repository.get_all_appointments.return_value = expected_appointments

        result = self.appointment_service.get_all_appointments()

        self.assertEqual(result, expected_appointments)

    def test_update_appointment_status_approved(self):
        self.appointment_service.update_appointment_status(
            1, 2, "approved"
        )

        self.appointment_service.appointment_repository.update_status.assert_called_once_with(
            1, 2, "approved"
        )

    def test_update_appointment_status_rejects_invalid_status(self):
        with self.assertRaises(InvalidAppointmentError):
            self.appointment_service.update_appointment_status(
                1, 2, "invalid"
            )


if __name__ == "__main__":
    unittest.main()