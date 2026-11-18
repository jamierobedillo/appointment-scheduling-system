
from models.user import User


class Customer(User):
    def __init__(self, full_name, email, phone):
        super().__init__(full_name, email, phone, "customer")

    def get_dashboard_message(self):
        return f"Welcome, {self.full_name}! You can book and manage your appointments here."
