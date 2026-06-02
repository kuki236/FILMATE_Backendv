from sqlalchemy.orm import Session, joinedload
from app.models.movie import Pelicula
from typing import List, Optional
import logging
from app.models.movie import Pelicula
from app.models.movie_genre import PeliculaGenero
from app.models.movie_actor import PeliculaActor
from app.models.movie_director import PeliculaDirector
from app.models.actor import Actor
from app.models.director import Director
from app.models.banner import BannerHome
from sqlalchemy import text

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


# ✅ CORRECTO
def list_movies(db: Session, skip: int = 0, limit: int = 100) -> List[Pelicula]:
    logger.info(f"📽️ Listando películas (skip={skip}, limit={limit})")
    try:
        movies = (
            db.query(Pelicula)
            .options(joinedload(Pelicula.generos))
            .filter(Pelicula.estado_registro == "Activo")
            .offset(skip)
            .limit(limit)
            .all()
        )
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


def update_movie(
    db: Session,
    movie_id: int,
    data: dict
):
    movie = db.query(Pelicula).filter(
        Pelicula.id_pelicula == movie_id
    ).first()

    if not movie:
        return None

    # =========================
    # ACTUALIZAR PELICULA
    # =========================

    movie.titulo = data["titulo"]
    movie.sinopsis = data["sinopsis"]
    movie.categoria_cartelera = data.get("categoria_cartelera")
    movie.duracion_minutos = data["duracion_minutos"]
    movie.clasificacion_edad = data["clasificacion_edad"]

    movie.categoria_cartelera = data["categoria_cartelera"]
    movie.estado_registro = data["estado_registro"]

    movie.url_poster = data["url_poster"]
    movie.url_trailer = data["url_trailer"]
    movie.url_banner = data.get("url_banner")

    # =========================
    # GENEROS
    # =========================

    db.query(PeliculaGenero).filter(
        PeliculaGenero.id_pelicula == movie_id
    ).delete()

    for genero_id in data["generos"]:
        nuevo_genero = PeliculaGenero(
            id_pelicula=movie_id,
            id_genero=genero_id
        )

        db.add(nuevo_genero)

    # =========================
    # ELENCO
    # =========================

    db.query(PeliculaActor).filter(
        PeliculaActor.id_pelicula == movie_id
    ).delete()

    for actor_data in data.get("elenco", []):

        actor = db.query(Actor).filter(
            Actor.nombre == actor_data["nombre"]
        ).first()

        if not actor:
            actor = Actor(
                nombre=actor_data["nombre"]
            )

            db.add(actor)
            db.flush()

        pelicula_actor = PeliculaActor(
            id_pelicula=movie_id,
            id_actor=actor.id_actor,
            personaje=actor_data["personaje"]
        )

        db.add(pelicula_actor)

    # =========================
    # DIRECTORES
    # =========================

    db.query(PeliculaDirector).filter(
        PeliculaDirector.id_pelicula == movie_id
    ).delete()

    for director_id in data.get("directores", []):
        nuevo_director = PeliculaDirector(
            id_pelicula=movie_id,
            id_director=director_id
        )
        db.add(nuevo_director)

    # =========================
    # BANNER
    # =========================

    url_banner = data.get("url_banner")

    if url_banner is not None and url_banner != "":

        banner = db.query(BannerHome).filter(
            BannerHome.id_pelicula == movie_id
        ).first()

        if banner:

            banner.imagen_url = url_banner

        else:

            nuevo_banner = BannerHome(
                id_pelicula=movie_id,
                imagen_url=url_banner,
                orden=1,
                is_activo=True
            )

            db.add(nuevo_banner)
    db.commit()
    db.refresh(movie)

    return movie

def delete_movie(db, movie_id):

    movie = db.query(Pelicula).filter(
        Pelicula.id_pelicula == movie_id
    ).first()

    if not movie:
        return None

    db.execute(text("""
        DELETE FROM pelicula_genero
        WHERE id_pelicula = :id
    """), {"id": movie_id})

    db.execute(text("""
        DELETE FROM pelicula_actor
        WHERE id_pelicula = :id
    """), {"id": movie_id})

    db.execute(text("""
        DELETE FROM pelicula_director
        WHERE id_pelicula = :id
    """), {"id": movie_id})

    db.execute(text("""
        DELETE FROM banner_home
        WHERE id_pelicula = :id
    """), {"id": movie_id})

    # eliminar película
    db.delete(movie)

    db.commit()

    return movie

