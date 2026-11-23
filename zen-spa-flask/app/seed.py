from app.app import app
from app.database import db
from app.models.user import User
from app.models.masaje import Masaje

with app.app_context():
    # Vaciar tablas si quieres empezar limpio
    db.drop_all()
    db.create_all()

    # ==========================
    # Crear usuarios de ejemplo
    # ==========================
    user1 = User(username="admin", email="admin@example.com", role="admin")
    user1.set_password("admin123")

    user2 = User(username="marta", email="marta@example.com", role="user")
    user2.set_password("marta123")

    user3 = User(username="pablo", email="pablo@example.com", role="user")
    user3.set_password("pablo123")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # ==========================
    # Crear masajes de ejemplo
    # ==========================
    masajes = [
        Masaje(
            nombre="Masaje relajante",
            duracion=60,
            precio=110,
            individual=False,
            filename=None,  # sin imagen
            user_id=user1.id
        ),
        Masaje(
            nombre="Masaje deportivo",
            duracion=45,
            precio=80,
            individual=False,
            filename=None,
            user_id=user2.id
        ),
        Masaje(
            nombre="Masaje con piedras calientes",
            duracion=75,
            precio=130,
            individual=True,
            filename=None,
            user_id=user1.id
        ),
        Masaje(
            nombre="Masaje aromaterapia",
            duracion=50,
            precio=100,
            individual=False,
            filename=None,
            user_id=user3.id
        )
    ]

    db.session.add_all(masajes)
    db.session.commit()

    print("Seeder ejecutado correctamente ✅")