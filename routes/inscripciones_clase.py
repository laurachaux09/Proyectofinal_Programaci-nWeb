from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection
import psycopg2

inscripciones_bp = Blueprint(
    "inscripciones_clase",
    __name__,
    url_prefix="/inscripciones"
)


def obtener_socios_y_clases(cur):
    cur.execute("""
        SELECT socio_id, documento, nombre, apellido
        FROM socio
        WHERE UPPER(estado) = 'ACTIVO'
        ORDER BY nombre, apellido;
    """)
    socios = cur.fetchall()

    cur.execute("""
        SELECT
            c.clase_id,
            c.nombre_clase,
            c.fecha_hora,
            c.cupo_maximo,
            esp.nombre_especialidad,
            e.nombre AS entrenador_nombre,
            e.apellido AS entrenador_apellido,
            (
                SELECT COUNT(*)
                FROM inscripcion_clase ic
                WHERE ic.clase_id = c.clase_id
                  AND UPPER(ic.estado) = 'INSCRITO'
            ) AS inscritos_actuales
        FROM clase c
        JOIN especialidad esp ON c.especialidad_id = esp.especialidad_id
        JOIN entrenador e ON c.entrenador_id = e.entrenador_id
        WHERE UPPER(c.estado) = 'PROGRAMADA'
        ORDER BY c.fecha_hora ASC;
    """)
    clases = cur.fetchall()
    return socios, clases


@inscripciones_bp.route("/")
def listar_inscripciones():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            ic.socio_id,
            ic.clase_id,
            s.documento,
            s.nombre AS socio_nombre,
            s.apellido AS socio_apellido,
            c.nombre_clase,
            c.fecha_hora,
            esp.nombre_especialidad,
            ic.fecha_inscripcion,
            ic.estado
        FROM inscripcion_clase ic
        JOIN socio s ON ic.socio_id = s.socio_id
        JOIN clase c ON ic.clase_id = c.clase_id
        JOIN especialidad esp ON c.especialidad_id = esp.especialidad_id
        ORDER BY ic.fecha_inscripcion DESC;
    """)
    inscripciones = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("inscripciones_clase/listar.html", inscripciones=inscripciones)


@inscripciones_bp.route("/crear", methods=["GET", "POST"])
def crear_inscripcion():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        socio_id = request.form.get("socio_id")
        clase_id = request.form.get("clase_id")
        estado = request.form.get("estado", "INSCRITO").upper()

        if not socio_id or not clase_id:
            flash("Debes seleccionar un socio y una clase.", "danger")
            socios, clases = obtener_socios_y_clases(cur)
            cur.close()
            conn.close()
            return render_template("inscripciones_clase/crear.html", socios=socios, clases=clases)

        try:
            cur.execute("""
                INSERT INTO inscripcion_clase (socio_id, clase_id, estado)
                VALUES (%s, %s, %s);
            """, (socio_id, clase_id, estado))
            conn.commit()
            cur.close()
            conn.close()
            flash("Inscripción registrada correctamente.", "success")
            return redirect(url_for("inscripciones_clase.listar_inscripciones"))

        
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash(
                "Este socio ya tiene una inscripción registrada para esta clase. "
                "Puedes consultar sus inscripciones y revisar su estado.",
                "warning"
            )

        except psycopg2.errors.RaiseException as e:
            conn.rollback()
            mensaje = e.diag.message_primary or "No se pudo completar la inscripción."
            flash(mensaje, "warning")

        except Exception:
            conn.rollback()
            flash(
                "Ocurrió un error inesperado al registrar la inscripción. "
                "Por favor, inténtalo nuevamente.",
                "danger"
            )


    socios, clases = obtener_socios_y_clases(cur)
    cur.close()
    conn.close()
    return render_template("inscripciones_clase/crear.html", socios=socios, clases=clases)


@inscripciones_bp.route("/editar/<int:socio_id>/<int:clase_id>", methods=["GET", "POST"])
def editar_inscripcion(socio_id, clase_id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        nuevo_estado = request.form.get("estado", "INSCRITO").upper()
        try:
            cur.execute("""
                UPDATE inscripcion_clase
                SET estado = %s
                WHERE socio_id = %s AND clase_id = %s;
            """, (nuevo_estado, socio_id, clase_id))
            conn.commit()
            cur.close()
            conn.close()
            flash("Estado de la inscripción actualizado correctamente.", "success")
            return redirect(url_for("inscripciones_clase.listar_inscripciones"))

        except Exception as e:
            conn.rollback()
            mensaje_error = str(e).splitlines()[0]
            flash(f"No se pudo actualizar la inscripción: {mensaje_error}", "danger")

    cur.execute("""
        SELECT
            ic.socio_id,
            ic.clase_id,
            s.documento,
            s.nombre,
            s.apellido,
            c.nombre_clase,
            c.fecha_hora,
            ic.fecha_inscripcion,
            ic.estado
        FROM inscripcion_clase ic
        JOIN socio s ON ic.socio_id = s.socio_id
        JOIN clase c ON ic.clase_id = c.clase_id
        WHERE ic.socio_id = %s AND ic.clase_id = %s;
    """, (socio_id, clase_id))
    inscripcion = cur.fetchone()
    cur.close()
    conn.close()

    if not inscripcion:
        flash("La inscripción solicitada no existe.", "danger")
        return redirect(url_for("inscripciones_clase.listar_inscripciones"))

    return render_template("inscripciones_clase/editar.html", inscripcion=inscripcion)


@inscripciones_bp.route("/eliminar/<int:socio_id>/<int:clase_id>", methods=["POST"])
def eliminar_inscripcion(socio_id, clase_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM inscripcion_clase
            WHERE socio_id = %s AND clase_id = %s;
        """, (socio_id, clase_id))
        conn.commit()
        flash("Inscripción eliminada correctamente.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error al eliminar la inscripción: {str(e).splitlines()[0]}", "danger")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("inscripciones_clase.listar_inscripciones"))