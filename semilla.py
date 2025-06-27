from app import db
from models.cancion import Cancion

db.create_all()

canciones = [
    Cancion(titulo='Shape of You', artista='Ed Sheeran', duracion=4.2),
    Cancion(titulo='Bohemian Rhapsody', artista='Queen', duracion=5.9),
    Cancion(titulo='Blinding Lights', artista='The Weeknd', duracion=3.3)
]

db.session.bulk_save_objects(canciones)
db.session.commit()

print("Canciones de ejemplo insertadas.")
