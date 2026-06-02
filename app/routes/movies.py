from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.dependencies import get_db
from sqlalchemy import distinct, text
from app.models.genre import Genero

from app.schemas.movie import (
    MovieCreate,
    MovieResponse,
    MovieUpdate,
    MovieDetailsResponse
)

from app.models.movie import Pelicula
from app.models.director import Director
from app.models.movie_director import PeliculaDirector
from app.repositories import movie_repository
from app.services.movie_service import get_movie_details

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)


@router.post("/", response_model=MovieResponse)
def create_movie(
    payload: MovieCreate,
    db: Session = Depends(get_db)
):
    logger.info(
        f"📥 POST /movies - Creando película: {payload.titulo}"
    )

    try:

        # ─────────────────────────────────────
        # Crear película principal
        # ─────────────────────────────────────
        movie = Pelicula(
            titulo=payload.titulo,
            sinopsis=payload.sinopsis,
            duracion_minutos=payload.duracion_minutos,
            clasificacion_edad=payload.clasificacion_edad,
            url_poster=payload.url_poster,
            url_trailer=payload.url_trailer,

            categoria_cartelera=payload.categoria_cartelera,
            estado_registro=payload.estado_registro
        )

        db.add(movie)
        db.commit()
        db.refresh(movie)

        # ─────────────────────────────────────
        # Guardar géneros
        # ─────────────────────────────────────
        for genero_id in payload.generos:

            db.execute(text(
                """
                INSERT INTO pelicula_genero (
                    id_pelicula,
                    id_genero
                )
                VALUES (:id_pelicula, :id_genero)
                """),
                {
                    "id_pelicula": movie.id_pelicula,
                    "id_genero": genero_id
                }
            )

        # ─────────────────────────────────────
        # Guardar actores/elenco
        # ─────────────────────────────────────
        for actor in payload.elenco:

            db.execute(text(
                """
                INSERT INTO pelicula_actor (
                    id_pelicula,
                    id_actor,
                    personaje
                )
                VALUES (
                    :id_pelicula,
                    :id_actor,
                    :personaje
                )
                """),
                {
                    "id_pelicula": movie.id_pelicula,
                    "id_actor": actor["id_actor"],
                    "personaje": actor["personaje"]
                }
            )

        # ─────────────────────────────────────
        # Guardar directores
        # ─────────────────────────────────────
        for director_id in payload.directores:
            db.execute(text(
                """
                INSERT INTO pelicula_director (
                    id_pelicula,
                    id_director
                )
                VALUES (:id_pelicula, :id_director)
                """),
                {
                    "id_pelicula": movie.id_pelicula,
                    "id_director": director_id
                }
            )

        # ─────────────────────────────────────
        # Guardar banner
        # ─────────────────────────────────────
        if payload.url_banner:

            db.execute(text(
                """
                INSERT INTO banner_home (
                    id_pelicula,
                    imagen_url,
                    orden,
                    is_activo
                )
                VALUES (
                    :id_pelicula,
                    :imagen_url,
                    1,
                    true
                )
                """),
                {
                    "id_pelicula": movie.id_pelicula,
                    "imagen_url": payload.url_banner
                }
            )

        db.commit()

        return movie

    except Exception as e:

        db.rollback()

        logger.error(
            f"❌ Error en POST /movies: {e}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/", response_model=List[MovieResponse])
def list_movies(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    logger.info(
        f"📥 GET /movies - skip={skip}, limit={limit}"
    )

    try:
        movies = movie_repository.list_movies(
            db,
            skip=skip,
            limit=limit
        )

        logger.info(
            f"✅ GET /movies completado, {len(movies)} resultados"
        )

        return movies

    except Exception as e:
        logger.error(
            f"❌ Error en GET /movies: {e}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"📥 GET /movies/{movie_id}")

    try:
        movie = movie_repository.get_movie(
            db,
            movie_id
        )

        if not movie:
            logger.warning(
                f"⚠️ Película no encontrada: {movie_id}"
            )

            raise HTTPException(
                status_code=404,
                detail="Movie not found"
            )

        return movie

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"❌ Error en GET /movies/{movie_id}: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    payload: MovieUpdate,
    db: Session = Depends(get_db)
):
    logger.info(f"📥 PUT /movies/{movie_id}")

    try:
        updated_movie = movie_repository.update_movie(
            db,
            movie_id,
            payload.dict()
        )

        if not updated_movie:
            raise HTTPException(
                status_code=404,
                detail="Movie not found"
            )

        logger.info(
            f"✅ Película actualizada: {movie_id}"
        )

        return updated_movie

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"❌ Error en PUT /movies/{movie_id}: {e}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"📥 DELETE /movies/{movie_id}")

    try:
        movie = movie_repository.get_movie(db, movie_id)

        if not movie:
            raise HTTPException(
                status_code=404,
                detail="Movie not found"
            )

        # ❌ NO BORRAR
        # db.delete(movie)

        # ✅ SOLO DESACTIVAR
        movie.estado_registro = "Inactivo"

        db.commit()
        db.refresh(movie)

        return {
            "message": "Movie deactivated successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"❌ Error en DELETE /movies/{movie_id}: {e}",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get(
    "/{movie_id}/details",
    response_model=MovieDetailsResponse
)
def movie_details(
    movie_id: int,
    db: Session = Depends(get_db)
):
    logger.info(
        "📥 GET /movies/%s/details",
        movie_id
    )

    return get_movie_details(
        db,
        movie_id
    )


# =========================================
# META - GÉNEROS
# =========================================

@router.get("/meta/genres")
def list_genres(
    db: Session = Depends(get_db)
):
    logger.info(
        "📥 GET /movies/meta/genres"
    )

    try:

        genres = (
            db.query(Genero)
            .order_by(Genero.nombre.asc())
            .all()
        )

        return genres

    except Exception as e:

        logger.error(
            f"❌ Error GET /movies/meta/genres: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# META - CLASIFICACIONES
# =========================================

@router.get("/meta/classifications")
def list_classifications(
    db: Session = Depends(get_db)
):
    logger.info(
        "📥 GET /movies/meta/classifications"
    )

    try:

        classifications = (
            db.query(
                distinct(
                    Pelicula.clasificacion_edad
                )
            )
            .filter(
                Pelicula.clasificacion_edad.isnot(None)
            )
            .all()
        )

        return [
            item[0]
            for item in classifications
        ]

    except Exception as e:

        logger.error(
            f"❌ Error GET /movies/meta/classifications: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# META - ESTADOS
# =========================================

@router.get("/meta/statuses")
def list_statuses(
    db: Session = Depends(get_db)
):
    logger.info(
        "📥 GET /movies/meta/statuses"
    )

    try:

        statuses = (
            db.query(
                distinct(
                    Pelicula.estado_registro
                )
            )
            .all()
        )

        return [
            item[0]
            for item in statuses
        ]

    except Exception as e:

        logger.error(
            f"❌ Error GET /movies/meta/statuses: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================
# META - DIRECTORES
# =========================================

@router.get("/meta/directors")
def list_directors_meta(db: Session = Depends(get_db)):
    logger.info("📥 GET /movies/meta/directors")
    try:
        directors = (
            db.query(Director)
            .order_by(Director.nombre.asc())
            .all()
        )
        return directors
    except Exception as e:
        logger.error(f"❌ Error GET /movies/meta/directors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# META - CATEGORÍAS
# =========================================

@router.get("/meta/categories")
def list_categories(
    db: Session = Depends(get_db)
):
    logger.info(
        "📥 GET /movies/meta/categories"
    )

    try:

        categories = (
            db.query(
                distinct(
                    Pelicula.categoria_cartelera
                )
            )
            .all()
        )

        return [
            item[0]
            for item in categories
        ]

    except Exception as e:

        logger.error(
            f"❌ Error GET /movies/meta/categories: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )