from flask import Blueprint, jsonify, request
from ..models.masaje import Masaje
from ..database import db
from ..schemas import MasajeDTO, MasajeCreateDTO
from pydantic import ValidationError
import asyncio
import httpx
from aiocache import cached, SimpleMemoryCache
import logging

logger = logging.getLogger(__name__)

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Caché de 10 minutos
@cached(ttl=600, cache=SimpleMemoryCache)
async def get_external_info(masaje_id: int):
    logger.info(f"Llamando API externa para masaje {masaje_id}")
    url = f"https://dummyjson.com/products/{masaje_id}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "external_name": data.get("title"),
                "external_price": data.get("price")
            }

    logger.warning(f"No se pudo obtener info externa para {masaje_id}")
    return {}

# GET todos
@api_v1.route('/masajes', methods=['GET'])
def get_masajes():
    logger.info("GET /masajes")

    try:
        masajes = Masaje.query.all()
        logger.info(f"Se obtuvieron {len(masajes)} masajes")

        return jsonify([MasajeDTO.from_orm(m).dict() for m in masajes])

    except Exception as e:
        logger.error(f"Error en GET /masajes: {str(e)}")
        return jsonify({"error": str(e)}), 500

# GET por ID
@api_v1.route('/masajes/<int:id>', methods=['GET'])
def get_masaje(id):
    logger.info(f"GET /masajes/{id}")

    try:
        masaje = db.session.get(Masaje, id)
        if not masaje:
            return jsonify({"error": "Masaje no encontrado"}), 404

        external_data = asyncio.run(get_external_info(id))

        result = MasajeDTO.from_orm(masaje).dict()
        result.update(external_data)

        logger.info(f"Masaje {id} obtenido correctamente")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error en GET /masajes/{id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# POST
@api_v1.route('/masajes', methods=['POST'])
def create_masaje():
    logger.info("POST /masajes")

    try:
        data = MasajeCreateDTO(**request.json)
    except ValidationError as e:
        logger.warning(f"Error de validación: {e.errors()}")
        return jsonify({"errors": e.errors()}), 400

    user_id = data.user_id

    usuario = db.session.execute(
        db.text("SELECT id FROM users WHERE id = :id"),
        {"id": user_id}
    ).fetchone()

    if not usuario:
        logger.warning("Usuario no existe, usando uno por defecto")

        usuario = db.session.execute(
            db.text("SELECT id FROM users LIMIT 1")
        ).fetchone()

        if not usuario:
            logger.error("No hay usuarios en la base de datos")
            return jsonify({"error": "No hay usuarios en la base de datos"}), 400

        user_id = usuario[0]

    masaje = Masaje(
        nombre=data.nombre,
        duracion=data.duracion,
        precio=data.precio,
        individual=data.individual,
        user_id=user_id,
        filename=data.filename
    )

    db.session.add(masaje)
    db.session.commit()

    logger.info(f"Masaje creado con ID {masaje.id}")

    return jsonify(MasajeDTO.from_orm(masaje).dict()), 201

# PUT
@api_v1.route('/masajes/<int:id>', methods=['PUT'])
def update_masaje(id):
    logger.info(f"PUT /masajes/{id}")

    masaje = db.session.get(Masaje, id)
    if not masaje:
        return jsonify({"error": "Masaje no encontrado"}), 404

    try:
        data = MasajeCreateDTO(**request.json)
    except ValidationError as e:
        logger.warning(f"Error de validación: {e.errors()}")
        return jsonify({"errors": e.errors()}), 400

    user_id = data.user_id

    usuario = db.session.execute(
        db.text("SELECT id FROM users WHERE id = :id"),
        {"id": user_id}
    ).fetchone()

    if not usuario:
        logger.warning("Usuario no existe en update, usando uno por defecto")

        usuario = db.session.execute(
            db.text("SELECT id FROM users LIMIT 1")
        ).fetchone()

        if not usuario:
            logger.error("No hay usuarios en la base de datos")
            return jsonify({"error": "No hay usuarios en la base de datos"}), 400

        user_id = usuario[0]

    masaje.nombre = data.nombre
    masaje.duracion = data.duracion
    masaje.precio = data.precio
    masaje.individual = data.individual
    masaje.user_id = user_id
    masaje.filename = data.filename

    db.session.commit()

    logger.info(f"Masaje {id} actualizado")

    return jsonify(MasajeDTO.from_orm(masaje).dict())

# DELETE
@api_v1.route('/masajes/<int:id>', methods=['DELETE'])
def delete_masaje(id):
    logger.info(f"DELETE /masajes/{id}")

    try:
        masaje = db.session.get(Masaje, id)
        if not masaje:
            return jsonify({"error": "Masaje no encontrado"}), 404

        db.session.delete(masaje)
        db.session.commit()

        logger.info(f"Masaje {id} eliminado")

        return jsonify({"message": "Eliminado"})

    except Exception as e:
        logger.error(f"Error en DELETE /masajes/{id}: {str(e)}")
        return jsonify({"error": str(e)}), 500