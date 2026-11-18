
from models.user import User


class Admin(User):
    def __init__(self, full_name, email, phone):
        super().__init__(full_name, email, phone, "admin")

    def get_dashboard_message(self):
        return f"Welcome, {self.full_name}! You can manage customers, services, and appointments here."
