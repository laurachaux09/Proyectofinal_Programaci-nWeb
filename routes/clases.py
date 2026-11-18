from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
from db import get_connection

clases_bp = Blueprint("clases", __name__, url_prefix="/clases")


@clases_bp.route("/")
def listar_clases():
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return render_template("clases/listar.html", clases=[])

    cur = conn.cursor()
    cur.execute("""
        SELECT c.clase_id,
               c.nombre_clase,
               c.descripcion,
               e.nombre || ' ' || e.apellido AS entrenador,
               es.nombre_especialidad AS especialidad_nombre,
               c.fecha_hora,
               c.duracion_minutos,
               c.cupo_maximo,
               c.estado
        FROM clase c
        JOIN entrenador e ON c.entrenador_id = e.entrenador_id
        JOIN especialidad es ON c.especialidad_id = es.especialidad_id
        ORDER BY e.nombre ASC, es.nombre_especialidad ASC
    """)
    clases = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("clases/listar.html", clases=clases)


def obtener_parejas_validas(cur):
    cur.execute("""
        SELECT ee.entrenador_id,
               ee.especialidad_id,
               e.nombre || ' ' || e.apellido || ' — ' || esp.nombre_especialidad AS etiqueta
        FROM entrenador_especialidad ee
        JOIN entrenador e ON ee.entrenador_id = e.entrenador_id
        JOIN especialidad esp ON ee.especialidad_id = esp.especialidad_id
        ORDER BY e.nombre ASC, esp.nombre_especialidad ASC
    """)
    return cur.fetchall()


@clases_bp.route("/crear", methods=["GET", "POST"])
def crear_clase():
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("clases.listar_clases"))

    cur = conn.cursor()

    if request.method == "POST":
        nombre_clase = request.form.get("nombre_clase", "").strip()
        descripcion = request.form.get("descripcion", "").strip() or None
        pareja = request.form.get("entrenador_especialidad", "")
        fecha_hora = request.form.get("fecha_hora", "").strip()
        duracion_minutos = request.form.get("duracion_minutos", "").strip()
        cupo_maximo = request.form.get("cupo_maximo", "").strip()
        estado = request.form.get("estado", "PROGRAMADA").strip().upper()

        if not nombre_clase or not pareja or not fecha_hora or not duracion_minutos or not cupo_maximo:
            flash("Todos los campos obligatorios deben completarse.", "warning")
        else:
            try:
                entrenador_id, especialidad_id = map(int, pareja.split("-"))
                fecha_sql = fecha_hora.replace("T", " ")

                cur.execute("""
                    INSERT INTO clase (
                        nombre_clase, descripcion, entrenador_id, especialidad_id,
                        fecha_hora, duracion_minutos, cupo_maximo, estado
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nombre_clase, descripcion, entrenador_id, especialidad_id,
                    fecha_sql, int(duracion_minutos), int(cupo_maximo), estado
                ))
                conn.commit()
                flash("Clase programada correctamente.", "success")
                cur.close()
                conn.close()
                return redirect(url_for("clases.listar_clases"))
            except psycopg2.Error as e:
                conn.rollback()
                flash(f"Error al registrar clase: {e.diag.message_primary or str(e)}", "danger")

    parejas = obtener_parejas_validas(cur)
    cur.close()
    conn.close()
    return render_template("clases/crear.html", parejas=parejas)


@clases_bp.route("/editar/<int:clase_id>", methods=["GET", "POST"])
def editar_clase(clase_id):
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("clases.listar_clases"))

    cur = conn.cursor()

    if request.method == "POST":
        nombre_clase = request.form.get("nombre_clase", "").strip()
        descripcion = request.form.get("descripcion", "").strip() or None
        pareja = request.form.get("entrenador_especialidad", "")
        fecha_hora = request.form.get("fecha_hora", "").strip()
        duracion_minutos = request.form.get("duracion_minutos", "").strip()
        cupo_maximo = request.form.get("cupo_maximo", "").strip()
        estado = request.form.get("estado", "PROGRAMADA").strip().upper()

        if not nombre_clase or not pareja or not fecha_hora or not duracion_minutos or not cupo_maximo:
            flash("Todos los campos obligatorios deben completarse.", "warning")
        else:
            try:
                entrenador_id, especialidad_id = map(int, pareja.split("-"))
                fecha_sql = fecha_hora.replace("T", " ")

                cur.execute("""
                    UPDATE clase
                    SET nombre_clase = %s,
                        descripcion = %s,
                        entrenador_id = %s,
                        especialidad_id = %s,
                        fecha_hora = %s,
                        duracion_minutos = %s,
                        cupo_maximo = %s,
                        estado = %s
                    WHERE clase_id = %s
                """, (
                    nombre_clase, descripcion, entrenador_id, especialidad_id,
                    fecha_sql, int(duracion_minutos), int(cupo_maximo), estado, clase_id
                ))
                conn.commit()
                flash("Clase actualizada correctamente.", "success")
                cur.close()
                conn.close()
                return redirect(url_for("clases.listar_clases"))
            except psycopg2.Error as e:
                conn.rollback()
                flash(f"Error al actualizar clase: {e.diag.message_primary or str(e)}", "danger")

    cur.execute("""
        SELECT clase_id, nombre_clase, descripcion, entrenador_id, especialidad_id,
               TO_CHAR(fecha_hora, 'YYYY-MM-DD"T"HH24:MI'), duracion_minutos, cupo_maximo, estado
        FROM clase
        WHERE clase_id = %s
    """, (clase_id,))
    clase = cur.fetchone()
    parejas = obtener_parejas_validas(cur)
    cur.close()
    conn.close()

    if not clase:
        flash("Clase no encontrada.", "warning")
        return redirect(url_for("clases.listar_clases"))

    return render_template("clases/editar.html", clase=clase, parejas=parejas)


@clases_bp.route("/eliminar/<int:clase_id>", methods=["POST"])
def eliminar_clase(clase_id):
    conn = get_connection()
    if conn is None:
        flash("Error de conexión con la base de datos.", "danger")
        return redirect(url_for("clases.listar_clases"))

    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM clase WHERE clase_id = %s", (clase_id,))
        conn.commit()
        flash("Clase eliminada correctamente.", "success")
    except psycopg2.IntegrityError:
        conn.rollback()
        flash("No se puede eliminar la clase porque tiene socios inscritos.", "danger")
    except psycopg2.Error as e:
        conn.rollback()
        flash(f"Error de base de datos: {e.diag.message_primary or str(e)}", "danger")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("clases.listar_clases"))