from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
import psycopg2

planes_bp = Blueprint("planes", __name__, url_prefix="/planes")


# LISTAR PLANES DE MEMBRESIA
@planes_bp.route("/")
def listar_planes():

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return render_template("planes_membresia/listar.html", planes=[])

    cursor = connection.cursor()

    cursor.execute("""
        SELECT plan_id, nombre_plan, descripcion,
               duracion_dias, precio, estado
        FROM plan_membresia
        ORDER BY plan_id;
    """)

    planes = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "planes_membresia/listar.html",
        planes=planes
    )



# REGISTRAR PLANES DE MEMBRESIA
@planes_bp.route("/crear", methods=["GET", "POST"])
def crear_plan():

    if request.method == "POST":

        nombre_plan = request.form.get("nombre_plan", "").strip()
        descripcion = request.form.get("descripcion", "").strip() or None
        duracion_dias = request.form.get("duracion_dias", "").strip()
        precio = request.form.get("precio", "").strip()
        estado = request.form.get("estado", "ACTIVO").strip().upper()

        # Validar campos obligatorios
        if not nombre_plan or not duracion_dias or not precio:
            flash("Completa todos los campos obligatorios.", "warning")
            return render_template("planes_membresia/crear.html")

        # Validar que duración y precio sean números
        try:
            duracion_dias = int(duracion_dias)
            precio = float(precio)

        except ValueError:
            flash("La duración y el precio deben ser números válidos.", "warning")
            return render_template("planes_membresia/crear.html")

        # Validar valores positivos
        if duracion_dias <= 0 or precio <= 0:
            flash("La duración y el precio deben ser mayores que cero.", "warning")
            return render_template("planes_membresia/crear.html")

        connection = get_connection()

        if connection is None:
            flash("Error de conexión con la base de datos.", "danger")
            return render_template("planes_membresia/crear.html")

        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO plan_membresia (
                    nombre_plan,
                    descripcion,
                    duracion_dias,
                    precio,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s);
            """, (
                nombre_plan,
                descripcion,
                duracion_dias,
                precio,
                estado
            ))

            connection.commit()

            flash("Plan de membresía registrado correctamente.", "success")

            return redirect(url_for("planes.listar_planes"))

        except psycopg2.IntegrityError:
            connection.rollback()

            flash("El nombre de ese plan ya existe o los datos incumplen una restricción.", "danger")

        except psycopg2.Error as error:
            connection.rollback()

            flash(f"Error de base de datos: {error}", "danger")

        finally:
            cursor.close()
            connection.close()

    return render_template("planes_membresia/crear.html")
# EDITAR PLANES DE MEMBRESIA
@planes_bp.route("/editar/<int:plan_id>", methods=["GET", "POST"])
def editar_plan(plan_id):

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("planes.listar_planes"))

    cursor = connection.cursor()

    try:

        # Buscar el plan que se desea editar
        cursor.execute("""
            SELECT plan_id, nombre_plan, descripcion,
                   duracion_dias, precio, estado
            FROM plan_membresia
            WHERE plan_id = %s;
        """, (plan_id,))

        plan = cursor.fetchone()

        if plan is None:
            flash("El plan que buscas no existe.", "warning")
            return redirect(url_for("planes.listar_planes"))

        # Si el formulario fue enviado
        if request.method == "POST":

            nombre_plan = request.form.get("nombre_plan", "").strip()
            descripcion = request.form.get("descripcion", "").strip() or None
            duracion_dias = request.form.get("duracion_dias", "").strip()
            precio = request.form.get("precio", "").strip()
            estado = request.form.get("estado", "ACTIVO").strip().upper()

            if not nombre_plan or not duracion_dias or not precio:
                flash("Completa todos los campos obligatorios.", "warning")

                return render_template(
                    "planes_membresia/editar.html",
                    plan=plan
                )

            try:
                duracion_dias = int(duracion_dias)
                precio = float(precio)

            except ValueError:
                flash("La duración y el precio deben ser números válidos.", "warning")

                return render_template(
                    "planes_membresia/editar.html",
                    plan=plan
                )

            if duracion_dias <= 0 or precio <= 0:
                flash("La duración y el precio deben ser mayores que cero.", "warning")

                return render_template(
                    "planes_membresia/editar.html",
                    plan=plan
                )

            # Actualizar los datos del plan
            cursor.execute("""
                UPDATE plan_membresia
                SET nombre_plan = %s,
                    descripcion = %s,
                    duracion_dias = %s,
                    precio = %s,
                    estado = %s
                WHERE plan_id = %s;
            """, (
                nombre_plan,
                descripcion,
                duracion_dias,
                precio,
                estado,
                plan_id
            ))

            connection.commit()

            flash("Plan actualizado correctamente.", "success")

            return redirect(url_for("planes.listar_planes"))

        # Si apenas se abre la página, mostrar los datos actuales
        return render_template(
            "planes_membresia/editar.html",
            plan=plan
        )

    except psycopg2.IntegrityError:
        connection.rollback()

        flash("El nombre del plan ya existe o los datos incumplen una restricción.", "danger")

        return render_template(
            "planes_membresia/editar.html",
            plan=plan
        )

    except psycopg2.Error as error:
        connection.rollback()

        flash(f"Error de base de datos: {error}", "danger")
        return redirect(url_for("planes.listar_planes"))

    finally:
        cursor.close()
        connection.close()
# DESACTIVAR PLANES DE MEMBRESIA
@planes_bp.route("/desactivar/<int:plan_id>", methods=["POST"])
def desactivar_plan(plan_id):

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("planes.listar_planes"))

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE plan_membresia
            SET estado = 'INACTIVO'
            WHERE plan_id = %s;
        """, (plan_id,))

        if cursor.rowcount > 0:
            connection.commit()
            flash("Plan desactivado correctamente.", "success")

        else:
            flash("El plan que intentas desactivar no existe.", "warning")

        return redirect(url_for("planes.listar_planes"))

    except psycopg2.Error as error:
        connection.rollback()
        flash(f"Error al desactivar el plan: {error}", "danger")
        return redirect(url_for("planes.listar_planes"))

    finally:
        cursor.close()
        connection.close()