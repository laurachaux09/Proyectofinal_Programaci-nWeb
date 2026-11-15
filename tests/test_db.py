
from db import get_connection


connection = get_connection()

if connection:
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT current_database(), current_user;
        """)

        resultado = cursor.fetchone()

        print("¡Conexion exitosa con PostgreSQL!")
        print("Base de datos:", resultado[0])
        print("Usuario:", resultado[1])

        cursor.close()
        connection.close()

    except Exception as error:
        print("Error al ejecutar la consulta:", error)

else:
    print("No fue posible establecer la conexion.")
