
class AppointmentError(Exception):
    """Base exception for appointment-related errors."""
    pass


class InvalidAppointmentError(AppointmentError):
    """Raised when appointment information is invalid."""
    pass


class AppointmentNotFoundError(AppointmentError):
    """Raised when an appointment cannot be found."""
    pass


class SlotUnavailableError(AppointmentError):
    """Raised when an appointment time slot is already taken."""
    pass


class AuthenticationError(AppointmentError):
    """Raised when login credentials are incorrect."""
    pass
