from flask import Blueprint, render_template, request, redirect, session, flash
from ..models.user import User
from ..database import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# LOGIN
@auth_bp.route("/login")
def login_form():
    return render_template("auth/login.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session["user_id"] = user.id
        session["role"] = user.role
        flash("Login correcto", "success")
        return redirect("/masajes/")
    else:
        flash("Email o contraseña incorrectos", "error")
        return redirect("/auth/login")


# LOGOUT
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect("/")


# REGISTER
@auth_bp.route("/register")
def register_form():
    return render_template("auth/register.html")


@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    flash("Usuario creado", "success")
    return redirect("/auth/login")
