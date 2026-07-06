import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_permiso
from app.models.seat import Asiento
from app.models.log_actividad_sistema import LogActividadSistema
from app.models.room import Sala
from app.schemas.seat import SeatCreate, SeatResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/seats", tags=["admin seats"])


@router.get("/room/{room_id}", response_model=List[SeatResponse], responses={404: {"description": "Sala no encontrada"}})
def admin_list_seats_by_room(
    room_id: int, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_ASIENTOS"))],
):
    sala = db.get(Sala, room_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return (
        db.query(Asiento)
        .filter(Asiento.id_sala == room_id, Asiento.eliminado == False)
        .order_by(Asiento.fila, Asiento.columna)
        .all()
    )


@router.post("/room/{room_id}/bulk", status_code=201, responses={404: {"description": "Sala no encontrada"}})
def bulk_create_seats(
    request: Request,
    room_id: int, payload: List[SeatCreate], db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_ASIENTOS"))],
):
    sala = db.get(Sala, room_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    created = []
    for seat_data in payload:
        seat = Asiento(
            id_sala=room_id,
            fila=seat_data.fila,
            columna=seat_data.columna,
            tipo_asiento=seat_data.tipo_asiento,
        )
        db.add(seat)
        created.append(seat)
    db.commit()
    for seat in created:
        db.refresh(seat)
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Asientos generados para sala {room_id}",
        modulo_afectado="ASIENTOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return created


@router.put("/{seat_id}", response_model=SeatResponse, responses={404: {"description": "Asiento no encontrado"}})
def update_seat(
    request: Request,
    seat_id: int, payload: SeatCreate, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_ASIENTOS"))],
):
    seat = db.get(Asiento, seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    seat.fila = payload.fila
    seat.columna = payload.columna
    seat.tipo_asiento = payload.tipo_asiento
    db.commit()
    db.refresh(seat)
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Asiento editado: {seat_id}",
        modulo_afectado="ASIENTOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return seat


@router.delete("/{seat_id}", responses={404: {"description": "Asiento no encontrado"}})
def delete_seat(
    request: Request,
    seat_id: int, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_ASIENTOS"))],
):
    seat = db.get(Asiento, seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    seat.eliminado = True
    from datetime import datetime
    seat.fecha_eliminacion = datetime.now()
    db.commit()
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Asiento eliminado: {seat_id}",
        modulo_afectado="ASIENTOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": "Asiento eliminado"}
