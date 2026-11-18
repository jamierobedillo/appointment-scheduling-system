
from werkzeug.security import generate_password_hash, check_password_hash

from models.customer import Customer
from models.admin import Admin
from repositories.user_repository import UserRepository
from exceptions.appointment_errors import AuthenticationError


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, full_name, email, phone, password):
        # Check required information
        if not full_name or not email or not phone or not password:
            raise ValueError("Please complete all required fields.")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        # Check if the email is already registered
        existing_user = self.user_repository.get_user_by_email(email)

        if existing_user:
            raise ValueError("This email is already registered.")

        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        user_id = self.user_repository.create_user(
            full_name,
            email,
            hashed_password,
            phone,
            "customer"
        )

        return user_id

    def login(self, email, password):
        # Find the account
        user_data = self.user_repository.get_user_by_email(email)

        if not user_data:
            raise AuthenticationError("Invalid email or password.")

        # Verify the hashed password
        if not check_password_hash(user_data["password"], password):
            raise AuthenticationError("Invalid email or password.")

        # Create the correct User child object
        if user_data["role"] == "admin":
            user = Admin(
                user_data["full_name"],
                user_data["email"],
                user_data["phone"]
            )
        else:
            user = Customer(
                user_data["full_name"],
                user_data["email"],
                user_data["phone"]
            )

        # Polymorphism: call the overridden method without checking the object type
        dashboard_message = user.get_dashboard_message()

        return {
            "user_id": user_data["user_id"],
            "user": user,
            "dashboard_message": dashboard_message
        }
