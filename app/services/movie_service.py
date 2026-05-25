from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.movie import Pelicula
from app.models.genre import Genero
from app.models.actor import Actor
from app.models.review import Resena
from app.models.movie_genre import PeliculaGenero
from app.models.movie_actor import PeliculaActor
from fastapi import HTTPException

def get_movie_details(db: Session, movie_id: int):

    movie = db.query(Pelicula).filter(
        Pelicula.id_pelicula == movie_id
    ).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    generos = (
        db.query(Genero.nombre)
        .join(PeliculaGenero,
              PeliculaGenero.id_genero == Genero.id_genero)
        .filter(PeliculaGenero.id_pelicula == movie_id)
        .all()
    )

    actores = (
        db.query(Actor.nombre, PeliculaActor.personaje)
        .join(PeliculaActor,
              PeliculaActor.id_actor == Actor.id_actor)
        .filter(PeliculaActor.id_pelicula == movie_id)
        .all()
    )

    stats = (
        db.query(
            func.avg(Resena.calificacion_estrellas),
            func.count(Resena.id_resena)
        )
        .filter(Resena.id_pelicula == movie_id)
        .first()
    )

    promedio = float(stats[0]) if stats[0] else 0.0
    total = stats[1] if stats[1] else 0

    return {
        "id_pelicula": movie.id_pelicula,
        "titulo": movie.titulo,
        "sinopsis": movie.sinopsis,
        "duracion_minutos": movie.duracion_minutos,
        "clasificacion_edad": movie.clasificacion_edad,
        "url_poster": movie.url_poster,
        "url_trailer": movie.url_trailer,
        "categoria_cartelera": movie.categoria_cartelera,

        "generos": generos,
        "actores": actores,

        "promedio_resenas": round(promedio, 1),
        "total_resenas": total
    }