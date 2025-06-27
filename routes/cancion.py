from flask import Blueprint, jsonify, request
from models.cancion import Cancion
from app import db

bp = Blueprint('canciones', __name__, url_prefix='/api/canciones')

@bp.route('/', methods=['GET'])
def listar_canciones():
    try:
        # Consulta ahora usa 'activo'
        canciones = Cancion.query.filter_by(activo=True).all()
        return jsonify([c.to_dict() for c in canciones])
    except Exception as e:
        return jsonify({"error": f"Error al listar canciones: {str(e)}"}), 500

@bp.route('/<int:id>', methods=['GET'])
def obtener_cancion(id):
    try:
        cancion = Cancion.query.get_or_404(id)
        # Verifica 'activo' aquí también
        if not cancion.activo:
            return jsonify({"mensaje": "Canción no encontrada o inactiva"}), 404
        return jsonify(cancion.to_dict())
    except Exception as e:
        return jsonify({"error": f"Error al obtener canción: {str(e)}"}), 500

@bp.route('/', methods=['POST'])
def crear_cancion():
    data = request.get_json()

    if not data or not all(key in data for key in ['cancion', 'artista', 'duracion']):
        return jsonify({"error": "Faltan datos obligatorios (cancion, artista, duracion)"}), 400

    try:
        nueva_cancion = Cancion(
            cancion=data['cancion'],
            artista=data['artista'],
            album=data.get('album'),
            anio=data.get('anio'),
            duracion=data['duracion'],
            fecha_lanzamiento=data.get('fecha_lanzamiento'),
            hora_estreno=data.get('hora_estreno'),
            descripcion=data.get('descripcion'),
            email_contacto=data.get('email_contacto'),
            activo=data.get('activo', True) # Usa 'activo' aquí
        )
        db.session.add(nueva_cancion)
        db.session.commit()

        return jsonify(nueva_cancion.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear canción: {str(e)}"}), 500

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_cancion(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

    try:
        cancion = Cancion.query.get_or_404(id)

        for key, value in data.items():
            if hasattr(cancion, key):
                setattr(cancion, key, value)

        db.session.commit()

        return jsonify(cancion.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar canción: {str(e)}"}), 500

@bp.route('/<int:id>/baja', methods=['PUT'])
def dar_de_baja(id):
    try:
        cancion = Cancion.query.get_or_404(id)
        # Verifica y cambia 'activo'
        if not cancion.activo:
            return jsonify({'mensaje': 'La canción ya está dada de baja o no existe.'}), 400
        cancion.activo = False
        db.session.commit()
        return jsonify({'mensaje': 'Canción dada de baja correctamente', 'id': id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al dar de baja la canción: {str(e)}"}), 500

@bp.route('/filtrar', methods=['GET'])
def filtrar_por_duracion():
    try:
        min_duracion = float(request.args.get('min', 0))
        max_duracion = float(request.args.get('max', float('inf')))

        canciones = Cancion.query.filter(
            Cancion.duracion >= min_duracion,
            Cancion.duracion <= max_duracion,
            Cancion.activo == True # Usa 'activo' aquí
        ).all()
        return jsonify([c.to_dict() for c in canciones])
    except ValueError:
        return jsonify({"error": "Los parámetros 'min' y 'max' deben ser números válidos."}), 400
    except Exception as e:
        return jsonify({"error": f"Error al filtrar canciones por duración: {str(e)}"}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_cancion_fisico(id):
    try:
        cancion = Cancion.query.get_or_404(id)
        db.session.delete(cancion)
        db.session.commit()
        return jsonify({'mensaje': 'Canción eliminada físicamente de la base de datos', 'id': id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la canción: {str(e)}"}), 500