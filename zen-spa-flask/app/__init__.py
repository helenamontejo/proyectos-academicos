import os
import logging
from flask import Flask, render_template, request, send_from_directory
from flasgger import Swagger
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists
from .database import db

# Blueprints
from .blueprints.masajes import masajes_bp
from .blueprints.usuarios import usuarios_bp
from .blueprints.auth import auth_bp
from .blueprints.api_v1 import api_v1

def create_app():
    app = Flask(__name__, static_folder="public", static_url_path="/public")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-desarrollo")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "DATABASE_URL",
        "mysql+mysqlconnector://USUARIO:CONTRASENA@localhost/zen_spa",
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
    )

    db.init_app(app)

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    Migrate(app, db)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(masajes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(api_v1)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")

    @app.route("/assets/<path:filename>")
    def assets(filename):
        return send_from_directory(ASSETS_FOLDER, filename)

    @app.before_request
    def method_override():
        if request.method == "POST":
            method = request.form.get("_method")
            if method:
                request.environ["REQUEST_METHOD"] = method.upper()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.errorhandler(404)
    def error_404(e):
        return "404 ERROR", 404

    @app.errorhandler(500)
    def error_500(e):
        print("ERROR 500:", e)
        return f"ERROR 500: {e}", 500

    # Swagger
    Swagger(app, template_file="openapi.yaml")

    return app
