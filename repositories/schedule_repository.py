
from database.connection import get_db_connection


class ScheduleRepository:

    def get_business_hours(self, day_of_week):
        connection = get_db_connection()
        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT opening_time, closing_time, is_closed
                FROM business_hours
                WHERE day_of_week = %s
            """, (day_of_week,))

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def check_slot_conflict(
        self,
        appointment_date,
        start_time,
        end_time
    ):
        connection = get_db_connection()
        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT appointment_id
                FROM appointments
                WHERE appointment_date = %s
                  AND status IN (%s, %s)
                  AND start_time < %s
                  AND end_time > %s
            """, (
                appointment_date,
                "pending",
                "approved",
                end_time,
                start_time
            ))

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            connection.close()
