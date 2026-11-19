from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

membresias_bp = Blueprint("membresias", __name__, url_prefix="/membresias")


# LISTAR MEMBRESIAS
@membresias_bp.route("/")
def listar_membresias():

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return render_template("membresias/listar.html", membresias=[])

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                m.membresia_id,
                s.nombre || ' ' || s.apellido AS socio,
                p.nombre_plan,
                m.fecha_inicio,
                m.fecha_fin,
                m.precio_contratado,
                m.estado
            FROM membresia m
            INNER JOIN socio s
                ON m.socio_id = s.socio_id
            INNER JOIN plan_membresia p
                ON m.plan_id = p.plan_id
            ORDER BY m.membresia_id;
        """)

        membresias = cursor.fetchall()

        return render_template(
            "membresias/listar.html",
            membresias=membresias
        )

    except Exception as error:
        flash(f"Error al consultar las membresías: {error}", "danger")
        return render_template("membresias/listar.html", membresias=[])

    finally:
        cursor.close()
        connection.close()

# REGISTRAR MEMBRESIAS
@membresias_bp.route("/crear", methods=["GET", "POST"])
def crear_membresia():

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("membresias.listar_membresias"))

    cursor = connection.cursor()

    try:

        # Consultar socios activos para el formulario
        cursor.execute("""
            SELECT socio_id, nombre, apellido
            FROM socio
            WHERE UPPER(estado) = 'ACTIVO'
            ORDER BY nombre, apellido;
        """)

        socios = cursor.fetchall()

        # Consultar planes activos para el formulario
        cursor.execute("""
            SELECT plan_id, nombre_plan, duracion_dias, precio
            FROM plan_membresia
            WHERE UPPER(estado) = 'ACTIVO'
            ORDER BY nombre_plan;
        """)

        planes = cursor.fetchall()

        if request.method == "POST":

            socio_id = request.form.get("socio_id", "")
            plan_id = request.form.get("plan_id", "")
            fecha_inicio_texto = request.form.get("fecha_inicio", "")

            if not socio_id or not plan_id or not fecha_inicio_texto:
                flash("Completa todos los campos obligatorios.", "warning")

                return render_template(
                    "membresias/crear.html",
                    socios=socios,
                    planes=planes
                )

            try:
                socio_id = int(socio_id)
                plan_id = int(plan_id)
                fecha_inicio = date.fromisoformat(fecha_inicio_texto)

            except ValueError:
                flash("Los datos seleccionados o la fecha no son válidos.", "warning")

                return render_template(
                    "membresias/crear.html",
                    socios=socios,
                    planes=planes
                )

            # Verificar que el socio exista y esté activo
            cursor.execute("""
                SELECT socio_id
                FROM socio
                WHERE socio_id = %s
                  AND UPPER(estado) = 'ACTIVO';
            """, (socio_id,))

            socio = cursor.fetchone()

            if socio is None:
                flash("El socio seleccionado no existe o está inactivo.", "warning")

                return render_template(
                    "membresias/crear.html",
                    socios=socios,
                    planes=planes
                )

            # Obtener la duración y el precio del plan
            cursor.execute("""
                SELECT duracion_dias, precio
                FROM plan_membresia
                WHERE plan_id = %s
                  AND UPPER(estado) = 'ACTIVO';
            """, (plan_id,))

            plan = cursor.fetchone()

            if plan is None:
                flash("El plan seleccionado no existe o está inactivo.", "warning")

                return render_template(
                    "membresias/crear.html",
                    socios=socios,
                    planes=planes
                )

            duracion_dias = plan[0]
            precio = Decimal(str(plan[1]))

            # Calcular fecha de vencimiento
            fecha_fin = fecha_inicio + timedelta(days=duracion_dias)

            # Insertar la membresía
            cursor.execute("""
                INSERT INTO membresia (
                    socio_id,
                    plan_id,
                    fecha_inicio,
                    fecha_fin,
                    precio_contratado,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                socio_id,
                plan_id,
                fecha_inicio,
                fecha_fin,
                precio,
                "ACTIVA"
            ))

            connection.commit()

            flash("Membresía registrada correctamente.", "success")

            return redirect(url_for("membresias.listar_membresias"))

        return render_template(
            "membresias/crear.html",
            socios=socios,
            planes=planes
        )

    except Exception as error:
        connection.rollback()
        flash(f"Error al registrar la membresía: {error}", "danger")

        return render_template(
            "membresias/crear.html",
            socios=socios,
            planes=planes
        )

    finally:
        cursor.close()
        connection.close()

# EDITAR MEMBRESIAS
@membresias_bp.route("/editar/<int:membresia_id>", methods=["GET", "POST"])
def editar_membresia(membresia_id):

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("membresias.listar_membresias"))

    cursor = connection.cursor()

    try:
        # Buscar la membresía que se desea editar
        cursor.execute("""
            SELECT membresia_id, socio_id, plan_id,
                   fecha_inicio, fecha_fin, precio_contratado, estado
            FROM membresia
            WHERE membresia_id = %s;
        """, (membresia_id,))

        membresia = cursor.fetchone()

        if membresia is None:
            flash("La membresía que buscas no existe.", "warning")
            return redirect(url_for("membresias.listar_membresias"))

        # Consultar socios y planes para los desplegables
        cursor.execute("""
            SELECT socio_id, nombre, apellido
            FROM socio
            ORDER BY nombre, apellido;
        """)
        socios = cursor.fetchall()

        cursor.execute("""
            SELECT plan_id, nombre_plan, duracion_dias, precio
            FROM plan_membresia
            ORDER BY nombre_plan;
        """)
        planes = cursor.fetchall()

        if request.method == "POST":

            socio_id = request.form.get("socio_id", "")
            plan_id = request.form.get("plan_id", "")
            fecha_inicio_texto = request.form.get("fecha_inicio", "")
            fecha_fin_texto = request.form.get("fecha_fin", "")
            precio_texto = request.form.get("precio_contratado", "").strip()
            estado = request.form.get("estado", "").upper()

            try:
                socio_id = int(socio_id)
                plan_id = int(plan_id)
                fecha_inicio = date.fromisoformat(fecha_inicio_texto)
                fecha_fin = date.fromisoformat(fecha_fin_texto)
                precio = Decimal(precio_texto)

            except (ValueError, TypeError, InvalidOperation):
                flash("Verifica los datos ingresados.", "warning")
                return render_template(
                    "membresias/editar.html",
                    membresia=membresia,
                    socios=socios,
                    planes=planes
                )

            if fecha_fin < fecha_inicio or precio <= 0:
                flash("La fecha de vencimiento debe ser igual o posterior al inicio y el precio debe ser positivo.", "warning")
                return render_template(
                    "membresias/editar.html",
                    membresia=membresia,
                    socios=socios,
                    planes=planes
                )

            if estado not in ("ACTIVA", "VENCIDA", "CANCELADA"):
                flash("El estado seleccionado no es válido.", "warning")
                return render_template(
                    "membresias/editar.html",
                    membresia=membresia,
                    socios=socios,
                    planes=planes
                )

            # Comprobar que el socio y el plan existan
            cursor.execute("""
                SELECT socio_id FROM socio
                WHERE socio_id = %s;
            """, (socio_id,))
            if cursor.fetchone() is None:
                flash("El socio seleccionado no existe.", "warning")
                return render_template(
                    "membresias/editar.html",
                    membresia=membresia,
                    socios=socios,
                    planes=planes
                )

            cursor.execute("""
                SELECT plan_id FROM plan_membresia
                WHERE plan_id = %s;
            """, (plan_id,))
            if cursor.fetchone() is None:
                flash("El plan seleccionado no existe.", "warning")
                return render_template(
                    "membresias/editar.html",
                    membresia=membresia,
                    socios=socios,
                    planes=planes
                )

            cursor.execute("""
                UPDATE membresia
                SET socio_id = %s,
                    plan_id = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    precio_contratado = %s,
                    estado = %s
                WHERE membresia_id = %s;
            """, (
                socio_id,
                plan_id,
                fecha_inicio,
                fecha_fin,
                precio,
                estado,
                membresia_id
            ))

            connection.commit()

            flash("Membresía actualizada correctamente.", "success")
            return redirect(url_for("membresias.listar_membresias"))

        return render_template(
            "membresias/editar.html",
            membresia=membresia,
            socios=socios,
            planes=planes
        )

    except Exception as error:
        connection.rollback()
        flash(f"Error al editar la membresía: {error}", "danger")
        return redirect(url_for("membresias.listar_membresias"))

    finally:
        cursor.close()
        connection.close()

# CANCELAR MEMBRESIAS
@membresias_bp.route("/cancelar/<int:membresia_id>", methods=["POST"])
def cancelar_membresia(membresia_id):

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("membresias.listar_membresias"))

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE membresia
            SET estado = 'CANCELADA'
            WHERE membresia_id = %s
              AND UPPER(estado) = 'ACTIVA';
        """, (membresia_id,))

        if cursor.rowcount > 0:
            connection.commit()
            flash("Membresía cancelada correctamente.", "success")
        else:
            connection.rollback()
            flash("No se encontró una membresía activa para cancelar.", "warning")

        return redirect(url_for("membresias.listar_membresias"))

    except Exception as error:
        connection.rollback()
        flash(f"Error al cancelar la membresía: {error}", "danger")
        return redirect(url_for("membresias.listar_membresias"))

    finally:
        cursor.close()
        connection.close()
