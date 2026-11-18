
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, full_name, email, phone, role):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.__role = role

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        if not value or not value.strip():
            raise ValueError("Full name cannot be empty.")

        self.__full_name = value.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not value or "@" not in value:
            raise ValueError("Please enter a valid email address.")

        self.__email = value.strip().lower()

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        if not value or not value.strip():
            raise ValueError("Phone number cannot be empty.")

        self.__phone = value.strip()

    @property
    def role(self):
        return self.__role

    @abstractmethod
    def get_dashboard_message(self):
        pass
