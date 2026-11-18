
import unittest
from unittest.mock import MagicMock, patch

from services.auth_service import AuthService
from exceptions.appointment_errors import AuthenticationError


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthService()
        self.auth_service.user_repository = MagicMock()

    @patch("services.auth_service.generate_password_hash")
    def test_register_successfully(self, mock_hash):
        mock_hash.return_value = "hashed_password"
        self.auth_service.user_repository.get_user_by_email.return_value = None
        self.auth_service.user_repository.create_user.return_value = 1

        user_id = self.auth_service.register(
            "Juan Dela Cruz",
            "juan@example.com",
            "09123456789",
            "Juan12345"
        )

        self.assertEqual(user_id, 1)
        self.auth_service.user_repository.create_user.assert_called_once()

    def test_register_rejects_empty_fields(self):
        with self.assertRaises(ValueError):
            self.auth_service.register(
                "",
                "juan@example.com",
                "09123456789",
                "Juan12345"
            )

    def test_register_rejects_short_password(self):
        with self.assertRaises(ValueError):
            self.auth_service.register(
                "Juan Dela Cruz",
                "juan@example.com",
                "09123456789",
                "123"
            )

    def test_register_rejects_existing_email(self):
        self.auth_service.user_repository.get_user_by_email.return_value = {
            "email": "juan@example.com"
        }

        with self.assertRaises(ValueError):
            self.auth_service.register(
                "Juan Dela Cruz",
                "juan@example.com",
                "09123456789",
                "Juan12345"
            )

    @patch("services.auth_service.check_password_hash")
    def test_customer_login_successfully(self, mock_check):
        mock_check.return_value = True

        self.auth_service.user_repository.get_user_by_email.return_value = {
            "user_id": 1,
            "full_name": "Juan Dela Cruz",
            "email": "juan@example.com",
            "password": "hashed_password",
            "phone": "09123456789",
            "role": "customer"
        }

        result = self.auth_service.login(
            "juan@example.com",
            "Juan12345"
        )

        self.assertEqual(result["user_id"], 1)
        self.assertEqual(result["user"].role, "customer")

    @patch("services.auth_service.check_password_hash")
    def test_admin_login_successfully(self, mock_check):
        mock_check.return_value = True

        self.auth_service.user_repository.get_user_by_email.return_value = {
            "user_id": 2,
            "full_name": "System Administrator",
            "email": "admin@example.com",
            "password": "hashed_password",
            "phone": "09123456789",
            "role": "admin"
        }

        result = self.auth_service.login(
            "admin@example.com",
            "Admin12345"
        )

        self.assertEqual(result["user_id"], 2)
        self.assertEqual(result["user"].role, "admin")

    def test_login_rejects_unknown_email(self):
        self.auth_service.user_repository.get_user_by_email.return_value = None

        with self.assertRaises(AuthenticationError):
            self.auth_service.login(
                "unknown@example.com",
                "WrongPassword"
            )

    @patch("services.auth_service.check_password_hash")
    def test_login_rejects_wrong_password(self, mock_check):
        mock_check.return_value = False

        self.auth_service.user_repository.get_user_by_email.return_value = {
            "user_id": 1,
            "full_name": "Juan Dela Cruz",
            "email": "juan@example.com",
            "password": "hashed_password",
            "phone": "09123456789",
            "role": "customer"
        }

        with self.assertRaises(AuthenticationError):
            self.auth_service.login(
                "juan@example.com",
                "WrongPassword"
            )


if __name__ == "__main__":
    unittest.main()
