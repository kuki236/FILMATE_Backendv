from sqlalchemy.orm import Session
from app.models.movie import Pelicula
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def get_movie(db: Session, movie_id: int) -> Optional[Pelicula]:
    logger.info(f"🔍 Buscando película con ID: {movie_id}")
    try:
        movie = db.query(Pelicula).filter(Pelicula.id_pelicula == movie_id).first()
        if movie:
            logger.info(f"✅ Película encontrada: {movie.titulo}")
        else:
            logger.warning(f"⚠️ Película no encontrada: {movie_id}")
        return movie
    except Exception as e:
        logger.error(f"❌ Error al buscar película: {e}")
        raise


def list_movies(db: Session, skip: int = 0, limit: int = 100) -> List[Pelicula]:
    logger.info(f"📽️ Listando películas (skip={skip}, limit={limit})")
    try:
        movies = db.query(Pelicula).offset(skip).limit(limit).all()
        logger.info(f"✅ Se obtuvieron {len(movies)} películas")
        return movies
    except Exception as e:
        logger.error(f"❌ Error al listar películas: {e}")
        raise


def create_movie(db: Session, movie: Pelicula) -> Pelicula:
    logger.info(f"➕ Creando película: {movie.titulo}")
    try:
        db.add(movie)
        db.commit()
        db.refresh(movie)
        logger.info(f"✅ Película creada exitosamente (ID: {movie.id_pelicula})")
        return movie
    except Exception as e:
        logger.error(f"❌ Error al crear película: {e}")
        db.rollback()
        raise


def update_movie(db: Session, movie_id: int, payload):
    movie = db.query(Pelicula).filter(
        Pelicula.id_pelicula == movie_id
    ).first()

    if not movie:
        return None

    movie.titulo = payload.titulo
    movie.sinopsis = payload.sinopsis
    movie.duracion_minutos = payload.duracion_minutos
    movie.clasificacion_edad = payload.clasificacion_edad
    movie.url_poster = payload.url_poster
    movie.url_trailer = payload.url_trailer

    db.commit()
    db.refresh(movie)

    return movie


def delete_movie(db: Session, movie_id: int):
    movie = db.query(Pelicula).filter(
        Pelicula.id_pelicula == movie_id
    ).first()

    if not movie:
        return None

    db.delete(movie)
    db.commit()

    return movie


def update_movie(db: Session, movie_id: int, data: dict):
    movie = db.query(Pelicula).filter(
        Pelicula.id_pelicula == movie_id
    ).first()

    if not movie:
        return None

    for key, value in data.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)

    return movie


def delete_movie(db: Session, movie_id: int):
    movie = db.query(Pelicula).filter(
        Pelicula.id_pelicula == movie_id
    ).first()

    if not movie:
        return None

    db.delete(movie)
    db.commit()

    return movie
