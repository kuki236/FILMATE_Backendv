"""Rutas de sedes/cines."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.cinema import Cine
from app.schemas.cinema import CinemaCreate, CinemaResponse

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


@router.post("/", response_model=CinemaResponse, status_code=201)
def create_cinema(payload: CinemaCreate, db: Session = Depends(get_db)):
    logger.info("📥 POST /cinemas - Creando cine: %s", payload.nombre)
    cinema = Cine(
        nombre=payload.nombre,
        direccion=payload.direccion,
        ciudad=payload.ciudad,
    )
    db.add(cinema)
    db.commit()
    db.refresh(cinema)
    return cinema


@router.put("/{cinema_id}", response_model=CinemaResponse)
def update_cinema(cinema_id: int, payload: CinemaCreate, db: Session = Depends(get_db)):
    logger.info("📥 PUT /cinemas/%s", cinema_id)
    cinema = db.get(Cine, cinema_id)
    if not cinema:
        raise HTTPException(status_code=404, detail="Cine no encontrado")
    cinema.nombre = payload.nombre
    cinema.direccion = payload.direccion
    cinema.ciudad = payload.ciudad
    db.commit()
    db.refresh(cinema)
    return cinema


@router.delete("/{cinema_id}")
def delete_cinema(cinema_id: int, db: Session = Depends(get_db)):
    logger.info("📥 DELETE /cinemas/%s", cinema_id)
    cinema = db.get(Cine, cinema_id)
    if not cinema:
        raise HTTPException(status_code=404, detail="Cine no encontrado")
    cinema.estado = False
    db.commit()
    return {"message": "Cine desactivado exitosamente"}
