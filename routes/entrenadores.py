from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
from db import get_connection

entrenadores_bp = Blueprint("entrenadores", __name__, url_prefix="/entrenadores")


@entrenadores_bp.route("/")
def listar_entrenadores():
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return render_template("entrenadores/listar.html", entrenadores=[])

    cur = conn.cursor()
    cur.execute("""
        SELECT entrenador_id, documento, nombre, apellido, telefono, correo, fecha_contratacion, estado
        FROM entrenador
        ORDER BY entrenador_id ASC
    """)
    entrenadores = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("entrenadores/listar.html", entrenadores=entrenadores)


@entrenadores_bp.route("/crear", methods=["GET", "POST"])
def crear_entrenador():
    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        telefono = request.form.get("telefono", "").strip() or None
        correo = request.form.get("correo", "").strip()
        estado = request.form.get("estado", "ACTIVO").strip().upper()

        if not documento or not nombre or not apellido or not correo:
            flash("Todos los campos obligatorios deben completarse.", "warning")
            return render_template("entrenadores/crear.html")

        conn = get_connection()
        if conn is None:
            flash("Error de conexión con la base de datos.", "danger")
            return render_template("entrenadores/crear.html")

        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO entrenador (documento, nombre, apellido, telefono, correo, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (documento, nombre, apellido, telefono, correo, estado))
            conn.commit()
            flash("Entrenador registrado correctamente.", "success")
            return redirect(url_for("entrenadores.listar_entrenadores"))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash("Error: El documento o correo ya está registrado en otro entrenador.", "danger")
        except psycopg2.Error as e:
            conn.rollback()
            flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")
        finally:
            cur.close()
            conn.close()

    return render_template("entrenadores/crear.html")


@entrenadores_bp.route("/editar/<int:entrenador_id>", methods=["GET", "POST"])
def editar_entrenador(entrenador_id):
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("entrenadores.listar_entrenadores"))

    cur = conn.cursor()

    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        telefono = request.form.get("telefono", "").strip() or None
        correo = request.form.get("correo", "").strip()
        estado = request.form.get("estado", "ACTIVO").strip().upper()

        try:
            cur.execute("""
                UPDATE entrenador
                SET documento = %s, nombre = %s, apellido = %s, telefono = %s,
                    correo = %s, estado = %s
                WHERE entrenador_id = %s
            """, (documento, nombre, apellido, telefono, correo, estado, entrenador_id))
            conn.commit()
            flash("Entrenador actualizado correctamente.", "success")
            cur.close()
            conn.close()
            return redirect(url_for("entrenadores.listar_entrenadores"))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash("Error: El documento o correo ya pertenece a otro entrenador.", "danger")
        except psycopg2.Error as e:
            conn.rollback()
            flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")

    cur.execute("""
        SELECT entrenador_id, documento, nombre, apellido, telefono, correo, fecha_contratacion, estado
        FROM entrenador
        WHERE entrenador_id = %s
    """, (entrenador_id,))
    entrenador = cur.fetchone()
    cur.close()
    conn.close()

    if not entrenador:
        flash("Entrenador no encontrado.", "warning")
        return redirect(url_for("entrenadores.listar_entrenadores"))

    return render_template("entrenadores/editar.html", entrenador=entrenador)


@entrenadores_bp.route("/eliminar/<int:entrenador_id>", methods=["POST"])
def eliminar_entrenador(entrenador_id):
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("entrenadores.listar_entrenadores"))

    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM entrenador WHERE entrenador_id = %s", (entrenador_id,))
        conn.commit()
        flash("Entrenador eliminado correctamente.", "success")
    except psycopg2.IntegrityError:
        conn.rollback()
        flash("No se puede eliminar el entrenador porque tiene especialidades o clases asignadas.", "danger")
    except psycopg2.Error as e:
        conn.rollback()
        flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("entrenadores.listar_entrenadores"))