
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
from decimal import Decimal, InvalidOperation

pagos_bp = Blueprint("pagos", __name__, url_prefix="/pagos")


@pagos_bp.route("/")
def listar_pagos():
    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return render_template("pagos/listar.html", pagos=[])

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                p.pago_id,
                s.nombre || ' ' || s.apellido AS socio,
                p.fecha_pago,
                p.monto,
                p.metodo_pago,
                p.estado
            FROM pago p
            INNER JOIN membresia m
                ON p.membresia_id = m.membresia_id
            INNER JOIN socio s
                ON m.socio_id = s.socio_id
            ORDER BY p.pago_id;
        """)

        pagos = cursor.fetchall()

        return render_template("pagos/listar.html", pagos=pagos)

    except Exception as error:
        flash(f"Error al consultar los pagos: {error}", "danger")
        return render_template("pagos/listar.html", pagos=[])

    finally:
        cursor.close()
        connection.close()

from decimal import Decimal, InvalidOperation


@pagos_bp.route("/crear", methods=["GET", "POST"])
def crear_pago():

    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("pagos.listar_pagos"))

    cursor = connection.cursor()

    try:
        if request.method == "POST":

            membresia_id = request.form.get("membresia_id")
            monto_texto = request.form.get("monto")
            metodo_pago = request.form.get("metodo_pago")
            estado = request.form.get("estado")

            # Validar los datos recibidos
            try:
                membresia_id = int(membresia_id)
                monto = Decimal(monto_texto)

            except (ValueError, TypeError, InvalidOperation):
                flash("Verifica los datos ingresados.", "warning")
                return redirect(url_for("pagos.crear_pago"))

            if monto <= 0:
                flash("El monto debe ser mayor que cero.", "warning")
                return redirect(url_for("pagos.crear_pago"))

            if metodo_pago not in ("EFECTIVO", "TARJETA", "TRANSFERENCIA"):
                flash("El método de pago seleccionado no es válido.", "warning")
                return redirect(url_for("pagos.crear_pago"))

            if estado not in ("PENDIENTE", "APROBADO", "RECHAZADO", "ANULADO"):
                flash("El estado seleccionado no es válido.", "warning")
                return redirect(url_for("pagos.crear_pago"))

            # Verificar que la membresía exista
            cursor.execute("""
                SELECT membresia_id
                FROM membresia
                WHERE membresia_id = %s;
            """, (membresia_id,))

            membresia = cursor.fetchone()

            if membresia is None:
                flash("La membresía seleccionada no existe.", "warning")
                return redirect(url_for("pagos.crear_pago"))

            # Registrar el pago
            cursor.execute("""
                INSERT INTO pago (
                    membresia_id,
                    monto,
                    metodo_pago,
                    estado
                )
                VALUES (%s, %s, %s, %s);
            """, (membresia_id, monto, metodo_pago, estado))

            connection.commit()

            flash("Pago registrado correctamente.", "success")
            return redirect(url_for("pagos.listar_pagos"))
        
        # Consultar membresías y sus saldos para el formulario
        cursor.execute("""
            SELECT
                m.membresia_id,
                s.nombre || ' ' || s.apellido AS socio,
                s.documento,
                p.nombre_plan,
                m.precio_contratado,
                COALESCE(
                    SUM(pg.monto) FILTER (
                        WHERE UPPER(pg.estado) = 'APROBADO'
                    ), 0
                ) AS total_pagado,
                m.precio_contratado - COALESCE(
                    SUM(pg.monto) FILTER (
                        WHERE UPPER(pg.estado) = 'APROBADO'
                    ), 0
                ) AS saldo_pendiente
            FROM membresia m
            INNER JOIN socio s
                ON m.socio_id = s.socio_id
            INNER JOIN plan_membresia p
                ON m.plan_id = p.plan_id
            LEFT JOIN pago pg
                ON m.membresia_id = pg.membresia_id
            GROUP BY
                m.membresia_id,
                s.nombre,
                s.apellido,
                s.documento,
                p.nombre_plan,
                m.precio_contratado
            ORDER BY m.membresia_id;
        """)

        membresias = cursor.fetchall()

        return render_template(
            "pagos/crear.html",
            membresias=membresias
        )

    except Exception as error:
        connection.rollback()
        flash(f"Error al registrar el pago: {error}", "danger")
        return redirect(url_for("pagos.listar_pagos"))

    finally:
        cursor.close()
        connection.close()
@pagos_bp.route("/editar/<int:pago_id>", methods=["GET", "POST"])
def editar_pago(pago_id):
    connection = get_connection()

    if connection is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("pagos.listar_pagos"))

    cursor = connection.cursor()

    try:
        if request.method == "POST":
            membresia_id = request.form.get("membresia_id")
            monto_texto = request.form.get("monto")
            metodo_pago = request.form.get("metodo_pago")
            estado = request.form.get("estado")

            try:
                membresia_id = int(membresia_id)
                monto = Decimal(monto_texto)
            except (ValueError, TypeError, InvalidOperation):
                flash("Verifica los datos ingresados.", "warning")
                return redirect(url_for("pagos.editar_pago", pago_id=pago_id))

            if not monto.is_finite() or monto <= 0:
                flash("El monto debe ser mayor que cero.", "warning")
                return redirect(url_for("pagos.editar_pago", pago_id=pago_id))

            if metodo_pago not in ("EFECTIVO", "TARJETA", "TRANSFERENCIA"):
                flash("El método de pago no es válido.", "warning")
                return redirect(url_for("pagos.editar_pago", pago_id=pago_id))

            if estado not in ("PENDIENTE", "APROBADO", "RECHAZADO", "ANULADO"):
                flash("El estado seleccionado no es válido.", "warning")
                return redirect(url_for("pagos.editar_pago", pago_id=pago_id))

            cursor.execute("""
                UPDATE pago
                SET membresia_id = %s,
                    monto = %s,
                    metodo_pago = %s,
                    estado = %s
                WHERE pago_id = %s;
            """, (membresia_id, monto, metodo_pago, estado, pago_id))

            if cursor.rowcount == 0:
                flash("El pago no existe.", "warning")
                return redirect(url_for("pagos.listar_pagos"))

            connection.commit()
            flash("Pago actualizado correctamente.", "success")
            return redirect(url_for("pagos.listar_pagos"))

        cursor.execute("""
            SELECT pago_id, membresia_id, monto, metodo_pago, estado
            FROM pago
            WHERE pago_id = %s;
        """, (pago_id,))

        pago = cursor.fetchone()

        if pago is None:
            flash("El pago no existe.", "warning")
            return redirect(url_for("pagos.listar_pagos"))

        # Consultar membresías para el formulario de edición
        cursor.execute("""
            SELECT
                m.membresia_id,
                s.nombre || ' ' || s.apellido AS socio,
                s.documento,
                p.nombre_plan
            FROM membresia m
            INNER JOIN socio s
                ON m.socio_id = s.socio_id
            INNER JOIN plan_membresia p
                ON m.plan_id = p.plan_id
            ORDER BY m.membresia_id;
        """)
        
        membresias = cursor.fetchall()

        return render_template(
            "pagos/editar.html",
            pago=pago,
            membresias=membresias
        )

    except Exception as error:
        connection.rollback()
        flash(f"Error al editar el pago: {error}", "danger")
        return redirect(url_for("pagos.listar_pagos"))

    finally:
        cursor.close()
        connection.close()
        