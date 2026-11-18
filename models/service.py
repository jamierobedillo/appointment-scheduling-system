
class Service:
    def __init__(self, service_name, description, duration, price):
        self.service_name = service_name
        self.description = description
        self.duration = duration
        self.price = price

    @property
    def service_name(self):
        return self.__service_name

    @service_name.setter
    def service_name(self, value):
        if not value or not value.strip():
            raise ValueError("Service name cannot be empty.")
        self.__service_name = value.strip()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value or ""

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Duration must be a positive number of minutes.")
        self.__duration = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = value
