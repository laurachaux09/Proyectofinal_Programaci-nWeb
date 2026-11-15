
from flask import Blueprint, render_template
from db import get_connection

socios_bp = Blueprint("socios", __name__)

@socios_bp.route("/socios")
def listar_socios():

    connection = get_connection()

    if connection is None:
        return "Error al conectar con la base de datos."

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM socio
            ORDER BY socio_id;
        """)

        socios = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template("socios/listar.html", socios=socios)

    except Exception as error:
        connection.close()
        return f"Error al consultar los socios: {error}"
