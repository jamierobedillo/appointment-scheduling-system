
import mariadb
from config import Config


def get_db_connection():
    """Create and return a connection to the MariaDB database."""
    try:
        connection = mariadb.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        return connection

    except mariadb.Error as error:
        print(f"Database connection error: {error}")
        raise
