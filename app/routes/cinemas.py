"""Rutas públicas de sedes/cines."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.cinema import Cine
from app.schemas.cinema import CinemaResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cinemas", tags=["cinemas"])


@router.get("/", response_model=List[CinemaResponse])
def list_cinemas(db: Session = Depends(get_db)):
    """Lista todas las sedes activas disponibles para el cliente."""

    logger.info("📥 GET /cinemas")
    try:
        return db.query(Cine).filter(Cine.estado.is_(True)).order_by(Cine.nombre).all()
    except Exception as exc:
        logger.error("❌ Error en GET /cinemas: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{cinema_id}", response_model=CinemaResponse)
def get_cinema(cinema_id: int, db: Session = Depends(get_db)):
    """Devuelve el detalle de una sede específica."""

    logger.info("📥 GET /cinemas/%s", cinema_id)
    try:
        cinema = db.get(Cine, cinema_id)
        if not cinema:
            raise HTTPException(status_code=404, detail="Cine no encontrado")
        return cinema
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("❌ Error en GET /cinemas/%s: %s", cinema_id, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
