from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
from db import get_connection

especialidades_bp = Blueprint("especialidades", __name__, url_prefix="/especialidades")


@especialidades_bp.route("/")
def listar_especialidades():
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return render_template("especialidades/listar.html", especialidades=[])

    cur = conn.cursor()
    cur.execute("""
        SELECT especialidad_id, nombre_especialidad, descripcion
        FROM especialidad
        ORDER BY especialidad_id ASC
    """)
    especialidades = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("especialidades/listar.html", especialidades=especialidades)


@especialidades_bp.route("/crear", methods=["GET", "POST"])
def crear_especialidad():
    if request.method == "POST":
        nombre = request.form.get("nombre_especialidad", "").strip()
        descripcion = request.form.get("descripcion", "").strip() or None

        if not nombre:
            flash("El nombre de la especialidad es obligatorio.", "warning")
            return render_template("especialidades/crear.html")

        conn = get_connection()
        if conn is None:
            flash("Error de conexión con la base de datos.", "danger")
            return render_template("especialidades/crear.html")

        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO especialidad (nombre_especialidad, descripcion)
                VALUES (%s, %s)
            """, (nombre, descripcion))
            conn.commit()
            flash("Especialidad registrada correctamente.", "success")
            return redirect(url_for("especialidades.listar_especialidades"))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash("Error: Ya existe una especialidad registrada con ese nombre.", "danger")
        except psycopg2.Error as e:
            conn.rollback()
            flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")
        finally:
            cur.close()
            conn.close()

    return render_template("especialidades/crear.html")


@especialidades_bp.route("/editar/<int:especialidad_id>", methods=["GET", "POST"])
def editar_especialidad(especialidad_id):
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("especialidades.listar_especialidades"))

    cur = conn.cursor()

    if request.method == "POST":
        nombre = request.form.get("nombre_especialidad", "").strip()
        descripcion = request.form.get("descripcion", "").strip() or None

        if not nombre:
            flash("El nombre de la especialidad es obligatorio.", "warning")
        else:
            try:
                cur.execute("""
                    UPDATE especialidad
                    SET nombre_especialidad = %s, descripcion = %s
                    WHERE especialidad_id = %s
                """, (nombre, descripcion, especialidad_id))
                conn.commit()
                flash("Especialidad actualizada correctamente.", "success")
                cur.close()
                conn.close()
                return redirect(url_for("especialidades.listar_especialidades"))
            except psycopg2.IntegrityError:
                conn.rollback()
                flash("Error: Ya existe otra especialidad con ese nombre.", "danger")
            except psycopg2.Error as e:
                conn.rollback()
                flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")

    cur.execute("""
        SELECT especialidad_id, nombre_especialidad, descripcion
        FROM especialidad
        WHERE especialidad_id = %s
    """, (especialidad_id,))
    especialidad = cur.fetchone()
    cur.close()
    conn.close()

    if not especialidad:
        flash("Especialidad no encontrada.", "warning")
        return redirect(url_for("especialidades.listar_especialidades"))

    return render_template("especialidades/editar.html", especialidad=especialidad)


@especialidades_bp.route("/eliminar/<int:especialidad_id>", methods=["POST"])
def eliminar_especialidad(especialidad_id):
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("especialidades.listar_especialidades"))

    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM especialidad WHERE especialidad_id = %s", (especialidad_id,))
        conn.commit()
        flash("Especialidad eliminada correctamente.", "success")
    except psycopg2.IntegrityError:
        conn.rollback()
        flash("No se puede eliminar la especialidad porque está asignada a entrenadores o clases.", "danger")
    except psycopg2.Error as e:
        conn.rollback()
        flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("especialidades.listar_especialidades"))