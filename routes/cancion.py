from flask import Blueprint, jsonify, request
from models.cancion import Cancion
from app import db

bp = Blueprint('canciones', __name__, url_prefix='/api/spotify/canciones')

@bp.route('/', methods=['GET'])
def get_all_active_songs():
    try:
        canciones = Cancion.query.filter_by(activo=True).all()
        return jsonify([c.to_dict() for c in canciones])
    except Exception as e:
        return jsonify({"error": f"Error al listar canciones activas: {str(e)}"}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def logical_delete_song(id):
    try:
        cancion = Cancion.query.get_or_404(id)
        if not cancion.activo:
            return jsonify({'mensaje': f'La canción con ID {id} ya está inactiva.'}), 200
        
        cancion.activo = False
        db.session.commit()
        return jsonify({'mensaje': f'Canción con ID {id} dada de baja correctamente (lógicamente).'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al dar de baja la canción: {str(e)}"}), 500

@bp.route('/clasificadas', methods=['GET'])
def get_classified_songs():
    try:
        all_active_songs = Cancion.query.filter_by(activo=True).all()
        
        clasificadas = {
            "Corta": [],
            "Media": [],
            "Larga": []
        }

        for cancion in all_active_songs:
            duracion = cancion.duracion
            if duracion < 180:
                clasificadas["Corta"].append(cancion.to_dict())
            elif 180 <= duracion <= 240:
                clasificadas["Media"].append(cancion.to_dict())
            elif duracion > 340:
                clasificadas["Larga"].append(cancion.to_dict())

        return jsonify(clasificadas)
    except Exception as e:
        return jsonify({"error": f"Error al clasificar canciones: {str(e)}"}), 500