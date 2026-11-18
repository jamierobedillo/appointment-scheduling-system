
import unittest
from datetime import date, time

from models.user import User
from models.customer import Customer
from models.admin import Admin
from models.service import Service
from models.appointment import Appointment
from models.appointment_manager import AppointmentManager


class TestUserModels(unittest.TestCase):

    def test_customer_creation(self):
        customer = Customer(
            "Juan Dela Cruz",
            "juan@example.com",
            "09123456789"
        )

        self.assertEqual(customer.full_name, "Juan Dela Cruz")
        self.assertEqual(customer.role, "customer")

    def test_admin_creation(self):
        admin = Admin(
            "System Administrator",
            "admin@example.com",
            "09123456789"
        )

        self.assertEqual(admin.role, "admin")

    def test_user_is_abstract(self):
        with self.assertRaises(TypeError):
            User("Juan", "juan@example.com", "09123456789", "customer")

    def test_customer_dashboard_message(self):
        customer = Customer(
            "Juan Dela Cruz",
            "juan@example.com",
            "09123456789"
        )

        self.assertIn("Welcome", customer.get_dashboard_message())

    def test_admin_dashboard_message(self):
        admin = Admin(
            "System Administrator",
            "admin@example.com",
            "09123456789"
        )

        self.assertIn(
    "administrator",
    admin.get_dashboard_message().lower()
)


class TestServiceModel(unittest.TestCase):

    def test_service_creation(self):
        service = Service(
            "General Consultation",
            "General health consultation",
            30,
            500
        )

        self.assertEqual(service.service_name, "General Consultation")
        self.assertEqual(service.duration, 30)
        self.assertEqual(service.price, 500)

    def test_service_rejects_empty_name(self):
        with self.assertRaises(ValueError):
            Service("", "Description", 30, 500)

    def test_service_rejects_invalid_duration(self):
        with self.assertRaises(ValueError):
            Service("Consultation", "Description", 0, 500)

    def test_service_rejects_negative_price(self):
        with self.assertRaises(ValueError):
            Service("Consultation", "Description", 30, -100)


class TestAppointmentModel(unittest.TestCase):

    def create_sample_appointment(self):
        service = Service(
            "General Consultation",
            "General consultation",
            30,
            500
        )

        return Appointment(
            user_id=1,
            service=service,
            appointment_date=date(2026, 11, 21),
            start_time=time(10, 0),
            end_time=time(10, 30),
            notes="Test appointment"
        )

    def test_appointment_creation(self):
        appointment = self.create_sample_appointment()

        self.assertEqual(appointment.user_id, 1)
        self.assertEqual(appointment.status, "pending")

    def test_appointment_rejects_invalid_user_id(self):
        with self.assertRaises(ValueError):
            Appointment(
                0,
                Service("Consultation", "", 30, 500),
                date(2026, 11, 21),
                time(10, 0),
                time(10, 30)
            )

    def test_appointment_rejects_invalid_status(self):
        appointment = self.create_sample_appointment()

        with self.assertRaises(ValueError):
            appointment.status = "completed"

    def test_appointment_rejects_invalid_end_time(self):
        with self.assertRaises(ValueError):
            Appointment(
                1,
                Service("Consultation", "", 30, 500),
                date(2026, 11, 21),
                time(10, 30),
                time(10, 0)
            )


class TestAppointmentManager(unittest.TestCase):

    def create_sample_appointment(self):
        service = Service(
            "General Consultation",
            "General consultation",
            30,
            500
        )

        return Appointment(
            1,
            service,
            date(2026, 11, 21),
            time(10, 0),
            time(10, 30)
        )

    def test_add_appointment(self):
        manager = AppointmentManager()
        appointment = self.create_sample_appointment()

        manager.add_appointment(appointment)

        self.assertEqual(manager.get_appointment_count(), 1)

    def test_manager_rejects_invalid_object(self):
        manager = AppointmentManager()

        with self.assertRaises(TypeError):
            manager.add_appointment("Not an appointment")

    def test_cancel_appointment(self):
        manager = AppointmentManager()
        appointment = self.create_sample_appointment()

        manager.add_appointment(appointment)
        manager.cancel_appointment(appointment)

        self.assertEqual(appointment.status, "cancelled")


if __name__ == "__main__":
    unittest.main()
