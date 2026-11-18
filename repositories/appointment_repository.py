
from database.connection import get_db_connection

from exceptions.appointment_errors import (
    AppointmentNotFoundError,
    InvalidAppointmentError
)


class AppointmentRepository:

    def create_appointment(self, appointment, service_id):
        connection = get_db_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO appointments (
                    user_id, service_id, appointment_date,
                    start_time, end_time, status, notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                appointment.user_id,
                service_id,
                appointment.appointment_date,
                appointment.start_time,
                appointment.end_time,
                appointment.status,
                appointment.notes
            ))

            appointment_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO appointment_logs (
                    appointment_id, user_id, action, description
                )
                VALUES (%s, %s, %s, %s)
            """, (
                appointment_id,
                appointment.user_id,
                "Created",
                "Customer created a new appointment."
            ))

            connection.commit()
            return appointment_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def get_customer_appointments(self, user_id):
        connection = get_db_connection()

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    a.appointment_id,
                    a.user_id,
                    a.service_id,
                    s.service_name,
                    s.price,
                    a.appointment_date,
                    a.start_time,
                    a.end_time,
                    a.status,
                    a.notes
                FROM appointments a
                JOIN services s ON a.service_id = s.service_id
                WHERE a.user_id = %s
                ORDER BY a.appointment_date DESC, a.start_time
            """, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def get_all_appointments(self):
        connection = get_db_connection()

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    a.appointment_id,
                    u.full_name,
                    u.email,
                    u.phone,
                    s.service_name,
                    s.price,
                    a.appointment_date,
                    a.start_time,
                    a.end_time,
                    a.status,
                    a.notes
                FROM appointments a
                JOIN users u ON a.user_id = u.user_id
                JOIN services s ON a.service_id = s.service_id
                ORDER BY a.appointment_date DESC, a.start_time
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def update_status(self, appointment_id, user_id, new_status):
        connection = get_db_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE appointments
                SET status = %s
                WHERE appointment_id = %s
            """, (new_status, appointment_id))

            if cursor.rowcount == 0:
                raise ValueError("Appointment not found.")

            cursor.execute("""
                INSERT INTO appointment_logs (
                    appointment_id, user_id, action, description
                )
                VALUES (%s, %s, %s, %s)
            """, (
                appointment_id,
                user_id,
                new_status,
                f"Appointment status changed to {new_status}."
            ))

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def cancel_customer_appointment(self, appointment_id, user_id):
        connection = get_db_connection()

        try:
            cursor = connection.cursor(dictionary=True)

            # Check whether this appointment belongs to the customer.
            cursor.execute("""
                SELECT status
                FROM appointments
                WHERE appointment_id = %s
                  AND user_id = %s
                FOR UPDATE
            """, (appointment_id, user_id))

            appointment = cursor.fetchone()

            if not appointment:
                raise AppointmentNotFoundError(
                    "Appointment not found."
                )

            if appointment["status"] != "pending":
                raise InvalidAppointmentError(
                    "Only pending appointments can be cancelled."
                )

            # Update appointment status.
            cursor.execute("""
                UPDATE appointments
                SET status = %s
                WHERE appointment_id = %s
                  AND user_id = %s
            """, ("cancelled", appointment_id, user_id))

            # Record cancellation in appointment logs.
            cursor.execute("""
                INSERT INTO appointment_logs (
                    appointment_id, user_id, action, description
                )
                VALUES (%s, %s, %s, %s)
            """, (
                appointment_id,
                user_id,
                "Cancelled",
                "Customer cancelled the appointment."
            ))

            connection.commit()
            return True

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def search_appointments(self, keyword):
        connection = get_db_connection()
        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            search_term = f"%{keyword}%"

            cursor.execute("""
                SELECT
                    a.appointment_id,
                    u.full_name,
                    u.email,
                    u.phone,
                    s.service_name,
                    s.price,
                    a.appointment_date,
                    a.start_time,
                    a.end_time,
                    a.status,
                    a.notes
                FROM appointments a
                JOIN users u ON a.user_id = u.user_id
                JOIN services s ON a.service_id = s.service_id
                WHERE u.full_name LIKE %s
                   OR u.email LIKE %s
                   OR s.service_name LIKE %s
                   OR a.status LIKE %s
                ORDER BY a.appointment_date DESC, a.start_time
            """, (
                search_term,
                search_term,
                search_term,
                search_term
            ))

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            connection.close()
