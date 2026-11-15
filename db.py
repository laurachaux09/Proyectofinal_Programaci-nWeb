
import psycopg2
from config import DB_CONFIG


def get_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection

    except psycopg2.Error as error:
        print("Error al conectar con PostgreSQL:", error)
        return None