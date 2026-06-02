"""Rutas para consultar funciones y horarios por sede."""

import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.showtime import Funcion
from app.repositories import showtime_repository
from app.core.dependencies import get_db
from app.schemas.showtime import (
    CinemaShowtimesResponse,
    ShowtimeCreate,
    ShowtimeResponse,
    ShowtimeUpdate
)
from typing import List
from app.services.showtime_service import (
    list_showtimes_by_cinema,
    list_showtimes_by_date,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/showtimes", tags=["showtimes"])


@router.get("/cinema/{cinema_id}", response_model=CinemaShowtimesResponse)
def get_showtimes_by_cinema(cinema_id: int, db: Session = Depends(get_db)):
    """Devuelve las películas y horarios disponibles en una sede."""

    logger.info("📥 GET /showtimes/cinema/%s", cinema_id)
    try:
        return list_showtimes_by_cinema(db, cinema_id)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("❌ Error en GET /showtimes/cinema/%s: %s", cinema_id, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


from app.schemas.showtime import ShowtimeResponse
from app.services.showtime_service import list_showtimes_by_movie

@router.get(
    "/movie/{movie_id}",
    response_model=list[ShowtimeResponse]
)
def get_showtimes_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """Devuelve todas las funciones de una película."""

    logger.info("📥 GET /showtimes/movie/%s", movie_id)

    try:
        return list_showtimes_by_movie(db, movie_id)

    except HTTPException:
        raise

    except Exception as exc:
        logger.error(
            "❌ Error en GET /showtimes/movie/%s: %s",
            movie_id,
            exc,
            exc_info=True
        )

        raise HTTPException(status_code=500, detail=str(exc))


@router.get(
    "/date/{target_date}",
    response_model=list[ShowtimeResponse]
)
def get_showtimes_by_date(
    target_date: date,
    cinema_id: int | None = None,
    movie_id: int | None = None,
    db: Session = Depends(get_db)
):
    """Devuelve funciones por fecha (`YYYY-MM-DD`) con filtros opcionales."""

    logger.info(
        "📥 GET /showtimes/date/%s?cinema_id=%s&movie_id=%s",
        target_date,
        cinema_id,
        movie_id,
    )

    try:
        return list_showtimes_by_date(
            db,
            target_date=target_date,
            cinema_id=cinema_id,
            movie_id=movie_id,
        )

    except Exception as exc:
        logger.error(
            "❌ Error en GET /showtimes/date/%s: %s",
            target_date,
            exc,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(exc))
    

@router.post("/", response_model=ShowtimeResponse)
def create_showtime(
    payload: ShowtimeCreate,
    db: Session = Depends(get_db)
):
    logger.info("📥 POST /showtimes")

    try:
        showtime = Funcion(
            id_pelicula=payload.id_pelicula,
            id_sala=payload.id_sala,
            fecha_hora_inicio=payload.fecha_hora_inicio,
            fecha_hora_fin=payload.fecha_hora_fin,
            idioma=payload.idioma,
            formato=payload.formato
        )

        created = showtime_repository.create_showtime(
            db,
            showtime
        )

        return created

    except Exception as e:
        logger.error(f"❌ Error POST /showtimes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/", response_model=List[ShowtimeResponse])
def list_all_showtimes(db: Session = Depends(get_db)):
    logger.info("📥 GET /showtimes")

    try:
        return showtime_repository.list_showtimes(db)

    except Exception as e:
        logger.error(f"❌ Error GET /showtimes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{showtime_id}", response_model=ShowtimeResponse)
def update_showtime(
    showtime_id: int,
    payload: ShowtimeUpdate,
    db: Session = Depends(get_db)
):
    logger.info(f"📥 PUT /showtimes/{showtime_id}")

    try:
        updated = showtime_repository.update_showtime(
            db,
            showtime_id,
            payload.dict()
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Showtime not found"
            )

        return updated

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"❌ Error PUT /showtimes/{showtime_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{showtime_id}")
def delete_showtime(
    showtime_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"📥 DELETE /showtimes/{showtime_id}")

    try:
        deleted = showtime_repository.delete_showtime(
            db,
            showtime_id
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Showtime not found"
            )

        return {
            "message": "Showtime deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"❌ Error DELETE /showtimes/{showtime_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
