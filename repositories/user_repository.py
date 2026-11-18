
from database.connection import get_db_connection


class UserRepository:

    def create_user(self, full_name, email, password, phone, role="customer"):
        connection = get_db_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO users (full_name, email, password, phone, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, email, password, phone, role))

            connection.commit()
            return cursor.lastrowid

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def get_user_by_email(self, email):
        connection = get_db_connection()

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT user_id, full_name, email, password, phone, role
                FROM users
                WHERE email = %s
            """, (email,))

            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    def get_all_customers(self):
        connection = get_db_connection()

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT user_id, full_name, email, phone
                FROM users
                WHERE role = %s
                ORDER BY full_name
            """, ("customer",))

            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    def create_admin(self, full_name, email, password, phone):
        return self.create_user(
            full_name,
            email,
            password,
            phone,
            "admin"
        )