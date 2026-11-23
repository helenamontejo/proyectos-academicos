from flask import Blueprint, render_template, request, redirect, g, flash
from ..models.user import User
from ..database import db

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

# Middleware: cargar usuario automáticamente
@usuarios_bp.url_value_preprocessor
def cargar_usuario(endpoint, values):
    if values and "id" in values:
        g.usuario = db.session.get(User, values["id"])
    else:
        g.usuario = None

# Listar usuarios
@usuarios_bp.route("/")
def listar():
    usuarios = User.query.all()
    return render_template("usuarios/list.html", usuarios=usuarios)

# Formulario nuevo
@usuarios_bp.route("/new")
def nuevo():
    return render_template("usuarios/new.html")

# Crear usuario
@usuarios_bp.route("/", methods=["POST"])
def crear():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role", "user")  # por defecto 'user' si no se indica

    if not username or not email or not password:
        flash("Debe completar todos los campos obligatorios.", "error")
        return redirect("/usuarios/new")

    # Crear usuario y asignar hash de contraseña
    usuario = User(username=username, email=email, role=role)
    usuario.set_password(password)

    db.session.add(usuario)
    db.session.commit()
    flash("Usuario creado correctamente", "success")
    return redirect("/usuarios/")

# Ver detalle
@usuarios_bp.route("/<string:id>")
def mostrar(id):
    if not g.usuario:
        return "Usuario no encontrado", 404
    return render_template("usuarios/show.html", usuario=g.usuario)

# Formulario editar
@usuarios_bp.route("/<string:id>/edit")
def editar(id):
    if not g.usuario:
        return "Usuario no encontrado", 404
    return render_template("usuarios/edit.html", usuario=g.usuario)

# Actualizar usuario
@usuarios_bp.route("/<string:id>/edit", methods=["POST"])
def actualizar(id):
    if not g.usuario:
        flash("Usuario no encontrado", "error")
        return redirect("/usuarios/")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    if not username or not email:
        flash("Username y email son obligatorios.", "error")
        return redirect(f"/usuarios/{id}/edit")

    g.usuario.username = username
    g.usuario.email = email
    g.usuario.role = role

    if password:
        g.usuario.set_password(password)

    db.session.commit()
    flash("Usuario actualizado correctamente", "success")
    return redirect("/usuarios/")

# Eliminar usuario
@usuarios_bp.route("/<string:id>/delete", methods=["POST"])
def eliminar(id):
    if g.usuario:
        db.session.delete(g.usuario)
        db.session.commit()
        flash("Usuario eliminado correctamente", "success")
    return redirect("/usuarios/")