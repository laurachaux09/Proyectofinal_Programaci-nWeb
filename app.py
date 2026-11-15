
from flask import Flask, render_template
from routes.socios import socios_bp

app = Flask(__name__)

app.register_blueprint(socios_bp)

@app.route("/")
def inicio():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)