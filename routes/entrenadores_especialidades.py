from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
from db import get_connection

entrenadores_esp_bp = Blueprint(
    "entrenadores_especialidades",
    __name__,
    url_prefix="/entrenadores-especialidades"
)


@entrenadores_esp_bp.route("/")
def listar():
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return render_template("entrenadores_especialidades/listar.html", asignaciones=[])

    cur = conn.cursor()
    cur.execute("""
        SELECT ee.entrenador_id,
               e.nombre || ' ' || e.apellido AS entrenador_nombre,
               ee.especialidad_id,
               e.nombre AS especialidad_nombre
        FROM entrenador_especialidad ee
        JOIN entrenador e ON ee.entrenador_id = e.entrenador_id
        JOIN especialidad es ON ee.especialidad_id = es.especialidad_id
        ORDER BY entrenador_nombre ASC, especialidad_nombre ASC
    """)
    asignaciones = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("entrenadores_especialidades/listar.html", asignaciones=asignaciones)


@entrenadores_esp_bp.route("/crear", methods=["GET", "POST"])
def crear():
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("entrenadores_especialidades.listar"))

    cur = conn.cursor()

    if request.method == "POST":
        entrenador_id = request.form.get("entrenador_id")
        especialidad_id = request.form.get("especialidad_id")

        if not entrenador_id or not especialidad_id:
            flash("Debes seleccionar un entrenador y una especialidad.", "warning")
        else:
            try:
                cur.execute("""
                    INSERT INTO entrenador_especialidad (entrenador_id, especialidad_id)
                    VALUES (%s, %s)
                """, (entrenador_id, especialidad_id))
                conn.commit()
                flash("Especialidad asignada al entrenador correctamente.", "success")
                cur.close()
                conn.close()
                return redirect(url_for("entrenadores_especialidades.listar"))
            except psycopg2.IntegrityError:
                conn.rollback()
                flash("Este entrenador ya tiene asignada esa especialidad.", "danger")
            except psycopg2.Error as e:
                conn.rollback()
                flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")

    cur.execute("SELECT entrenador_id, nombre, apellido FROM entrenador ORDER BY nombre ASC")
    entrenadores = cur.fetchall()

    cur.execute("SELECT especialidad_id, nombre_especialidad AS nombre FROM especialidad ORDER BY nombre_especialidad ASC")
    cur.execute("SELECT especialidad_id, nombre_especialidad AS nombre FROM especialidad ORDER BY nombre_especialidad ASC")
    especialidades = cur.fetchall()
    cur.close()
    cur.close()
    conn.close()
    return render_template(
        "entrenadores_especialidades/crear.html",
        entrenadores=entrenadores,
        especialidades=especialidades
    )


@entrenadores_esp_bp.route("/eliminar/<int:entrenador_id>/<int:especialidad_id>", methods=["POST"])
def eliminar(entrenador_id, especialidad_id):
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("entrenadores_especialidades.listar"))

    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM entrenador_especialidad
            WHERE entrenador_id = %s AND especialidad_id = %s
        """, (entrenador_id, especialidad_id))
        conn.commit()
        flash("Asignación eliminada correctamente.", "success")
    except psycopg2.IntegrityError:
        conn.rollback()
        flash("No se puede eliminar porque existen clases programadas con este entrenador y especialidad.", "danger")
    except psycopg2.Error as e:
        conn.rollback()
        flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("entrenadores_especialidades.listar"))