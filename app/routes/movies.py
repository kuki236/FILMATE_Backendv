from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from app.core.dependencies import get_db
from app.schemas.movie import (
    MovieCreate,
    MovieResponse,
    MovieUpdate
)
from app.models.movie import Pelicula
from app.repositories import movie_repository
from app.schemas.movie import MovieDetailsResponse
from app.services.movie_service import get_movie_details

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/movies", tags=["movies"])


@router.post("/", response_model=MovieResponse)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    logger.info(f"📥 POST /movies - Creando película: {payload.titulo}")
    try:
        movie = Pelicula(
            titulo=payload.titulo,
            sinopsis=payload.sinopsis,
            duracion_minutos=payload.duracion_minutos,
            clasificacion_edad=payload.clasificacion_edad,
            url_poster=payload.url_poster,
            url_trailer=payload.url_trailer
        )

        created = movie_repository.create_movie(db, movie)
        return created
    except Exception as e:
        logger.error(f"❌ Error en POST /movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[MovieResponse])
def list_movies(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    logger.info(f"📥 GET /movies - skip={skip}, limit={limit}")
    try:
        movies = movie_repository.list_movies(db, skip=skip, limit=limit)
        logger.info(f"✅ GET /movies completado, {len(movies)} resultados")
        return movies
    except Exception as e:
        logger.error(f"❌ Error en GET /movies: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    logger.info(f"📥 GET /movies/{movie_id}")
    try:
        movie = movie_repository.get_movie(db, movie_id)
        if not movie:
            logger.warning(f"⚠️ Película no encontrada: {movie_id}")
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except Exception as e:
        logger.error(f"❌ Error en GET /movies/{movie_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    payload: MovieCreate,
    db: Session = Depends(get_db)
):
    logger.info(f"📥 PUT /movies/{movie_id}")

    try:
        updated_movie = movie_repository.update_movie(
            db,
            movie_id,
            payload
        )

        if not updated_movie:
            raise HTTPException(
                status_code=404,
                detail="Movie not found"
            )

        logger.info(f"✅ Película actualizada: {movie_id}")

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
        deleted_movie = movie_repository.delete_movie(
            db,
            movie_id
        )

        if not deleted_movie:
            raise HTTPException(
                status_code=404,
                detail="Movie not found"
            )

        logger.info(f"✅ Película eliminada: {movie_id}")

        return {
            "message": "Movie deleted successfully"
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

        return updated_movie

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"❌ Error en PUT /movies/{movie_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"📥 DELETE /movies/{movie_id}")

    try:
        deleted_movie = movie_repository.delete_movie(
            db,
            movie_id
        )

        if not deleted_movie:
            raise HTTPException(
                status_code=404,
                detail="Movie not found"
            )

        return {
            "message": "Movie deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"❌ Error en DELETE /movies/{movie_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/{movie_id}/details",
    response_model=MovieDetailsResponse
)
def movie_details(movie_id: int, db: Session = Depends(get_db)):
    """Devuelve información completa de una película."""
    
    logger.info("📥 GET /movies/%s/details", movie_id)

    return get_movie_details(db, movie_id)