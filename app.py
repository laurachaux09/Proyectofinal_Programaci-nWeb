
from flask import Flask, render_template
from routes.socios import socios_bp
from routes.entrenadores import entrenadores_bp
from routes.especialidades import especialidades_bp

from config import SECRET_KEY
app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(socios_bp)
app.register_blueprint(entrenadores_bp)
app.register_blueprint(especialidades_bp)

@app.route("/")
def inicio():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)