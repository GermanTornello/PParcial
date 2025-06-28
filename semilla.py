from app import create_app, db
from models.cancion import Cancion
from datetime import date, time

app = create_app()

with app.app_context():
    if Cancion.query.count() == 0:
        canciones = [
            Cancion(
                cancion='Shape of You', 
                artista='Ed Sheeran',
                album='÷ (Divide)',
                anio=2017,
                duracion=233,
                fecha_lanzamiento=date(2017, 1, 6),
                hora_estreno=time(0, 0, 0),
                descripcion='Un éxito pop global con influencias tropicales.',
                email_contacto='edsheeran@music.com',
                activo=True
            ),
            Cancion(
                cancion='Bohemian Rhapsody', 
                artista='Queen',
                album='A Night at the Opera',
                anio=1975,
                duracion=354,
                fecha_lanzamiento=date(1975, 10, 31),
                hora_estreno=time(12, 0, 0),
                descripcion='Una ópera rock icónica y compleja.',
                email_contacto=None,
                activo=True
            ),
            Cancion(
                cancion='Blinding Lights', 
                artista='The Weeknd',
                album='After Hours',
                anio=2019,
                duracion=200,
                fecha_lanzamiento=date(2019, 11, 29),
                hora_estreno=time(9, 0, 0),
                descripcion='Sintetizadores de los 80 con ritmos contemporáneos.',
                email_contacto='theweeknd@xo.com',
                activo=True
            )
        ]

        db.session.bulk_save_objects(canciones)
        db.session.commit()
        print("Canciones de ejemplo insertadas.")
    else:
        print("Ya existen canciones en la base de datos, omitiendo inserción de ejemplo.")

