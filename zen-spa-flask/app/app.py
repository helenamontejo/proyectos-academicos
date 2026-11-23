import os
from flask import Flask, render_template, request, send_from_directory
from .blueprints.masajes import masajes_bp
from .blueprints.usuarios import usuarios_bp
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists
from .database import db
from .blueprints.auth import auth_bp

app = Flask(__name__, static_folder="public", static_url_path="/public")

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-desarrollo")

# CONFIGURAR BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "mysql+mysqlconnector://USUARIO:CONTRASENA@localhost/zen_spa",
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)

# Crear base de datos si no existe
if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

migrate = Migrate(app, db)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Esto apunta a la carpeta app/
ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")       # Carpeta assets dentro de app/

@app.route("/assets/<path:filename>")
def assets(filename):
    """Sirve archivos desde la carpeta assets"""
    return send_from_directory(ASSETS_FOLDER, filename)

@app.before_request
def method_override():
    if request.method == "POST":
        method = request.form.get("_method")
        if method:
            request.environ["REQUEST_METHOD"] = method.upper()

app.register_blueprint(masajes_bp)
app.register_blueprint(usuarios_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def error_404(e):
    return render_template("error404.html"), 404


@app.errorhandler(500)
def error_500(e):
    return render_template("error500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
