from flask import Flask, render_template
from db import get_connection
from routes.socios import socios_bp
from routes.entrenadores import entrenadores_bp
from routes.especialidades import especialidades_bp
from routes.entrenadores_especialidades import entrenadores_esp_bp
from routes.clases import clases_bp
from routes.planes_membresia import planes_bp
from routes.membresias import membresias_bp
from routes.pagos import pagos_bp
from routes.inscripciones_clase import inscripciones_bp

from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(planes_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(entrenadores_bp)
app.register_blueprint(especialidades_bp)
app.register_blueprint(entrenadores_esp_bp)
app.register_blueprint(clases_bp)
app.register_blueprint(membresias_bp)
app.register_blueprint(pagos_bp)
app.register_blueprint(inscripciones_bp)


@app.route("/")
def inicio():
    stats = {
        "socios_activos": 0,
        "membresias_activas": 0,
        "clases_programadas": 0,
        "ingresos_totales": 0
    }
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM socio WHERE UPPER(estado) = 'ACTIVO';")
        stats["socios_activos"] = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM membresia
            WHERE UPPER(estado) = 'ACTIVA'
              AND CURRENT_DATE BETWEEN fecha_inicio AND fecha_fin;
        """)
        stats["membresias_activas"] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM clase WHERE UPPER(estado) = 'PROGRAMADA';")
        stats["clases_programadas"] = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(monto), 0) FROM pago WHERE UPPER(estado) = 'APROBADO';")
        stats["ingresos_totales"] = cur.fetchone()[0]

        cur.close()
        conn.close()
    except Exception:
        pass

    return render_template("index.html", stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
