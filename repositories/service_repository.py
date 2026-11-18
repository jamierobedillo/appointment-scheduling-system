
from database.connection import get_db_connection
from models.service import Service


class ServiceRepository:

    def get_all_services(self):
        connection = get_db_connection()

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT service_id, service_name, description,
                       duration, price, status
                FROM services
                WHERE status = %s
                ORDER BY service_name
            """, ("Active",))

            rows = cursor.fetchall()

            return [
                {
                    "service_id": row["service_id"],
                    "service": Service(
                        row["service_name"],
                        row["description"],
                        row["duration"],
                        row["price"]
                    )
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()
