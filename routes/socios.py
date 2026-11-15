from flask import Blueprint, render_template, request, redirect, url_for
from db import get_connection
import psycopg2

socios_bp = Blueprint("socios", __name__)


# CONSULTAR SOCIOS
@socios_bp.route("/socios")
def listar_socios():

    connection = get_connection()

    if connection is None:
        return "Error al conectar con la base de datos."

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                socio_id,
                documento,
                nombre,
                apellido,
                telefono,
                correo,
                fecha_nacimiento,
                fecha_registro,
                estado
            FROM socio
            ORDER BY socio_id;
        """)

        socios = cursor.fetchall()

        return render_template(
            "socios/listar.html",
            socios=socios
        )

    except Exception as error:
        return f"Error al consultar los socios: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


# REGISTRAR SOCIOS
@socios_bp.route("/socios/nuevo", methods=["GET", "POST"])
def crear_socio():

    if request.method == "POST":

        documento = request.form["documento"].strip()
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        telefono = request.form["telefono"].strip() or None
        correo = request.form["correo"].strip() or None
        fecha_nacimiento = request.form["fecha_nacimiento"]
        estado = request.form["estado"]

        if not documento or not nombre or not apellido or not fecha_nacimiento:
            return render_template(
                "socios/crear.html",
                mensaje="Completa todos los campos obligatorios."
            )

        connection = get_connection()

        if connection is None:
            return "Error al conectar con la base de datos."

        cursor = None

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO socio (
                    documento,
                    nombre,
                    apellido,
                    telefono,
                    correo,
                    fecha_nacimiento,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
                documento,
                nombre,
                apellido,
                telefono,
                correo,
                fecha_nacimiento,
                estado
            ))

            connection.commit()

            return redirect(url_for("socios.listar_socios"))

        except psycopg2.errors.UniqueViolation:
            connection.rollback()

            return render_template(
                "socios/crear.html",
                mensaje="El documento o el correo ya están registrados."
            )

        except Exception as error:
            connection.rollback()
            return f"Error al registrar el socio: {error}"

        finally:
            if cursor is not None:
                cursor.close()

            connection.close()

    return render_template("socios/crear.html")
# EDITAR SOCIOS
@socios_bp.route("/socios/editar/<int:socio_id>", methods=["GET", "POST"])
def editar_socio(socio_id):

    connection = get_connection()

    if connection is None:
        return "Error al conectar con la base de datos."

    cursor = None

    try:
        cursor = connection.cursor()

        # Cuando se envía el formulario
        if request.method == "POST":

            documento = request.form["documento"].strip()
            nombre = request.form["nombre"].strip()
            apellido = request.form["apellido"].strip()
            telefono = request.form["telefono"].strip() or None
            correo = request.form["correo"].strip() or None
            fecha_nacimiento = request.form["fecha_nacimiento"]
            estado = request.form["estado"]

            if not documento or not nombre or not apellido or not fecha_nacimiento:
                cursor.execute("""
                    SELECT * FROM socio
                    WHERE socio_id = %s;
                """, (socio_id,))

                socio = cursor.fetchone()

                return render_template(
                    "socios/editar.html",
                    socio=socio,
                    mensaje="Completa todos los campos obligatorios."
                )

            cursor.execute("""
                UPDATE socio
                SET documento = %s,
                    nombre = %s,
                    apellido = %s,
                    telefono = %s,
                    correo = %s,
                    fecha_nacimiento = %s,
                    estado = %s
                WHERE socio_id = %s;
            """, (
                documento,
                nombre,
                apellido,
                telefono,
                correo,
                fecha_nacimiento,
                estado,
                socio_id
            ))

            connection.commit()

            return redirect(url_for("socios.listar_socios"))

        # Cuando se abre la página por primera vez
        cursor.execute("""
            SELECT *
            FROM socio
            WHERE socio_id = %s;
        """, (socio_id,))

        socio = cursor.fetchone()

        if socio is None:
            return "El socio que intentas editar no existe."

        return render_template(
            "socios/editar.html",
            socio=socio
        )

    except psycopg2.errors.UniqueViolation:
        connection.rollback()

        cursor.execute("""
            SELECT *
            FROM socio
            WHERE socio_id = %s;
        """, (socio_id,))

        socio = cursor.fetchone()

        return render_template(
            "socios/editar.html",
            socio=socio,
            mensaje="El documento o el correo ya están registrados."
        )

    except Exception as error:
        connection.rollback()
        return f"Error al editar el socio: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
# DESACTIVAR SOCIOS
@socios_bp.route("/socios/eliminar/<int:socio_id>", methods=["POST"])
def eliminar_socio(socio_id):

    connection = get_connection()

    if connection is None:
        return "Error al conectar con la base de datos."

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE socio
            SET estado = 'INACTIVO'
            WHERE socio_id = %s;
        """, (socio_id,))

        connection.commit()

        return redirect(url_for("socios.listar_socios"))

    except Exception as error:
        connection.rollback()
        return f"Error al desactivar el socio: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()