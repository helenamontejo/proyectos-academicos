import os
import uuid
from flask import request, flash
from PIL import Image

# Carpetas dentro de app
UPLOAD_FOLDER = "app/assets/images"
THUMBNAIL_FOLDER = "app/assets/thumbnails"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Crear carpetas si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Comprueba que la extensión sea válida"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file():
    """Guarda la imagen subida y crea un thumbnail"""
    file = request.files.get("image")

    if not file or file.filename == "":
        return None

    # Validar extensión
    if not allowed_file(file.filename):
        flash("Formato no permitido.", "error")
        return None

    # Validar tamaño
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE:
        flash("La imagen supera los 5MB.", "error")
        return None

    # Generar nombre UUID
    extension = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4()}.{extension}"

    # Guardar imagen original
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Crear thumbnail (200x200)
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, filename)
    with Image.open(filepath) as img:
        img.thumbnail((200, 200))
        img.save(thumbnail_path)

    return filename

def delete_file(filename):
    """Borra imagen y thumbnail"""
    if not filename:
        return

    # Imagen original
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(image_path):
        os.remove(image_path)

    # Thumbnail
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, filename)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
 