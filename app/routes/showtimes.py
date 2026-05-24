"""Rutas para consultar funciones y horarios por sede."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.showtime import CinemaShowtimesResponse
from app.services.showtime_service import list_showtimes_by_cinema

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
