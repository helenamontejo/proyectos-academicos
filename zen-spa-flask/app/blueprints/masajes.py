from flask import Blueprint, render_template, request, redirect, g, flash, session, abort
from ..handle_files import save_file, delete_file
from ..models.masaje import Masaje
from ..database import db

masajes_bp = Blueprint("masajes", __name__, url_prefix="/masajes")

# Middleware: cargar masaje automáticamente
@masajes_bp.url_value_preprocessor
def cargar_masaje(endpoint, values):
    if values and "id" in values:
        g.masaje = db.session.get(Masaje, int(values["id"]))
    else:
        g.masaje = None

# Listar masajes
@masajes_bp.route("/")
def listar():
    if session.get("role") == "admin":
        resultado = Masaje.query
    elif session.get("user_id"):
        resultado = Masaje.query.filter_by(user_id=session.get("user_id"))
    else:
        resultado = Masaje.query.filter_by(user_id=None)  # nadie logueado → vacío

    nombre = request.args.get("nombre", "").strip()
    rango = request.args.get("precio")

    if nombre:
        resultado = resultado.filter(Masaje.nombre.contains(nombre))
    if rango == "menor100":
        resultado = resultado.filter(Masaje.precio < 100)
    elif rango == "entre100y120":
        resultado = resultado.filter(Masaje.precio.between(100,120))
    elif rango == "mayor120":
        resultado = resultado.filter(Masaje.precio > 120)

    return render_template("masajes/list.html", masajes=resultado.all())

# Formulario nuevo
@masajes_bp.route("/new")
def nuevo():
    if not session.get("user_id"):
        flash("Debes iniciar sesión", "error")
        return redirect("/auth/login")
    return render_template("masajes/new.html")

# Crear masaje
@masajes_bp.route("/", methods=["POST"])
def crear():
    if not session.get("user_id"):
        flash("Debes iniciar sesión", "error")
        return redirect("/auth/login")

    nombre = request.form.get("nombre").strip()
    duracion = int(request.form.get("duracion"))
    precio = int(request.form.get("precio"))
    individual = "individual" in request.form
    user_id = session.get("user_id")

    filename = save_file()

    nuevo = Masaje(
        nombre=nombre,
        duracion=duracion,
        precio=precio,
        individual=individual,
        filename=filename,
        user_id=user_id
    )

    db.session.add(nuevo)
    db.session.commit()
    flash("Masaje creado correctamente", "success")
    return redirect("/masajes/")

# Ver detalle
@masajes_bp.route("/<int:id>")
def mostrar(id):
    if not g.masaje:
        return "Masaje no encontrado", 404

    # RBAC: user normal solo puede ver sus masajes
    if session.get("role") != "admin" and g.masaje.user_id != session.get("user_id"):
        abort(403)

    return render_template("masajes/show.html", masaje=g.masaje)

# Formulario editar
@masajes_bp.route("/<int:id>/edit")
def editar(id):
    if not g.masaje:
        flash("Masaje no encontrado", "error")
        return redirect("/masajes/")

    # RBAC: user normal solo puede editar sus masajes
    if session.get("role") != "admin" and g.masaje.user_id != session.get("user_id"):
        abort(403)

    return render_template("masajes/edit.html", masaje=g.masaje)

# Actualizar masaje
@masajes_bp.route("/<int:id>/edit", methods=["POST"])
def actualizar(id):
    if not g.masaje:
        flash("Masaje no encontrado", "error")
        return redirect("/masajes/")

    # RBAC
    if session.get("role") != "admin" and g.masaje.user_id != session.get("user_id"):
        abort(403)

    g.masaje.nombre = request.form.get("nombre").strip()
    g.masaje.duracion = int(request.form.get("duracion"))
    g.masaje.precio = int(request.form.get("precio"))
    g.masaje.individual = "individual" in request.form

    filename = save_file()
    if filename:
        delete_file(g.masaje.filename)
        g.masaje.filename = filename

    db.session.commit()
    flash("Masaje actualizado correctamente", "success")
    return redirect("/masajes/")

# Eliminar masaje
@masajes_bp.route("/<int:id>/delete", methods=["POST"])
def eliminar(id):
    if not g.masaje:
        flash("Masaje no encontrado", "error")
        return redirect("/masajes/")

    # RBAC
    if session.get("role") != "admin" and g.masaje.user_id != session.get("user_id"):
        abort(403)

    delete_file(g.masaje.filename)
    db.session.delete(g.masaje)
    db.session.commit()
    flash("Masaje eliminado correctamente", "success")
    return redirect("/masajes/")
