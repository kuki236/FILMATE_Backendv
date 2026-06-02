"""Rutas para consulta y bloqueo de asientos en tiempo real."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.seat import Asiento
from app.models.room import Sala
from app.schemas.seat import SeatCreate, SeatLockRequest, SeatLockResponse, SeatMapResponse, SeatResponse
from app.services.seat_service import get_showtime_seat_map, lock_showtime_seats

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/seats", tags=["seats"])


@router.get("/showtime/{showtime_id}", response_model=SeatMapResponse)
def get_seat_map(showtime_id: int, db: Session = Depends(get_db)):
    """Lista los asientos de una función con su estado actual."""

    logger.info("📥 GET /seats/showtime/%s", showtime_id)
    try:
        return get_showtime_seat_map(db, showtime_id)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("❌ Error en GET /seats/showtime/%s: %s", showtime_id, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


# =========================================
# ADMIN - GESTIÓN DE ASIENTOS POR SALA
# =========================================

@router.get("/room/{room_id}", response_model=List[SeatResponse])
def list_seats_by_room(room_id: int, db: Session = Depends(get_db)):
    sala = db.get(Sala, room_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return db.query(Asiento).filter(Asiento.id_sala == room_id).order_by(Asiento.fila, Asiento.numero).all()


@router.post("/room/{room_id}/bulk", status_code=201)
def bulk_create_seats(room_id: int, payload: List[SeatCreate], db: Session = Depends(get_db)):
    sala = db.get(Sala, room_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    created = []
    for seat_data in payload:
        seat = Asiento(
            id_sala=room_id,
            fila=seat_data.fila,
            numero=seat_data.numero,
            coord_x=seat_data.coord_x,
            coord_y=seat_data.coord_y,
        )
        db.add(seat)
        created.append(seat)
    db.commit()
    for seat in created:
        db.refresh(seat)
    return created


@router.put("/{seat_id}", response_model=SeatResponse)
def update_seat(seat_id: int, payload: SeatCreate, db: Session = Depends(get_db)):
    seat = db.get(Asiento, seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    seat.fila = payload.fila
    seat.numero = payload.numero
    seat.coord_x = payload.coord_x
    seat.coord_y = payload.coord_y
    db.commit()
    db.refresh(seat)
    return seat


@router.delete("/{seat_id}")
def delete_seat(seat_id: int, db: Session = Depends(get_db)):
    seat = db.get(Asiento, seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    db.delete(seat)
    db.commit()
    return {"message": "Asiento eliminado"}


@router.post("/lock", response_model=SeatLockResponse)
def lock_seats(payload: SeatLockRequest, db: Session = Depends(get_db)):
    """Bloquea asientos para una función en una transacción consistente."""

    logger.info("📥 POST /seats/lock - función=%s asientos=%s", payload.id_funcion, payload.ids_asientos)
    try:
        return lock_showtime_seats(db, payload.id_funcion, payload.ids_asientos)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("❌ Error en POST /seats/lock: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
