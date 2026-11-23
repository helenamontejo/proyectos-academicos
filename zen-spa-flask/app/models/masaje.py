from ..database import db

class Masaje(db.Model):
    __tablename__ = "masajes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    individual = db.Column(db.Boolean, default=False)
    filename = db.Column(db.String(120), nullable=True)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))