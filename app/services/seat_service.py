"""Servicios de asientos: mapa por función y bloqueo transaccional."""

import asyncio
from typing import List

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models.seat import Asiento
from app.models.showtime import Funcion
from app.models.showtime_seat import FuncionAsiento
from app.schemas.seat import SeatLockResponse, SeatMapResponse, ShowtimeSeatItem
from app.websocket.seats_ws import publish_showtime_update


def get_showtime_seat_map(db: Session, showtime_id: int) -> SeatMapResponse:
    """Obtiene el mapa de asientos de una función con su estado actual."""

    showtime = db.get(Funcion, showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="Función no encontrada")

    stmt = (
        select(Asiento, FuncionAsiento.estado)
        .outerjoin(
            FuncionAsiento,
            and_(
                FuncionAsiento.id_asiento == Asiento.id_asiento,
                FuncionAsiento.id_funcion == showtime_id,
            ),
        )
        .where(Asiento.id_sala == showtime.id_sala)
        .order_by(Asiento.fila, Asiento.numero)
    )

    rows = db.execute(stmt).all()
    asientos = [
        ShowtimeSeatItem(
            id_asiento=seat.id_asiento,
            fila=seat.fila,
            numero=seat.numero,
            estado=estado or "Disponible",
        )
        for seat, estado in rows
    ]

    return SeatMapResponse(
        id_funcion=showtime.id_funcion,
        id_sala=showtime.id_sala,
        asientos=asientos,
    )


def set_showtime_seats_state(
    db: Session,
    showtime_id: int,
    seat_ids: List[int],
    new_state: str,
) -> List[Asiento]:
    """Cambia el estado de asientos de una función de forma consistente."""

    unique_ids = sorted(set(seat_ids))
    if not unique_ids:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un asiento")

    showtime = db.get(Funcion, showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="Función no encontrada")

    seats = db.execute(
        select(Asiento)
        .where(
            Asiento.id_sala == showtime.id_sala,
            Asiento.id_asiento.in_(unique_ids),
        )
        .with_for_update()
    ).scalars().all()

    if len(seats) != len(unique_ids):
        raise HTTPException(status_code=404, detail="Uno o más asientos no pertenecen a la sala")

    existing_rows = db.execute(
        select(FuncionAsiento)
        .where(
            FuncionAsiento.id_funcion == showtime_id,
            FuncionAsiento.id_asiento.in_(unique_ids),
        )
        .with_for_update()
    ).scalars().all()

    existing_by_id = {row.id_asiento: row for row in existing_rows}

    for seat_id in unique_ids:
        current = existing_by_id.get(seat_id)
        if current is None:
            db.add(
                FuncionAsiento(
                    id_funcion=showtime_id,
                    id_asiento=seat_id,
                    estado=new_state,
                )
            )
            continue

        if current.estado == "Vendido":
            raise HTTPException(status_code=409, detail=f"El asiento {seat_id} ya fue vendido")

        if current.estado == "Reservado" and new_state == "Reservado":
            raise HTTPException(status_code=409, detail=f"El asiento {seat_id} ya está reservado")

        current.estado = new_state

    db.flush()
    return seats


def lock_showtime_seats(db: Session, showtime_id: int, seat_ids: List[int]) -> SeatLockResponse:
    """Bloquea asientos en tiempo real para una función."""

    with db.begin():
        locked_seats = set_showtime_seats_state(db, showtime_id, seat_ids, "Reservado")

    publish_current_seat_map(db, showtime_id)
    return SeatLockResponse(
        id_funcion=showtime_id,
        ids_asientos_bloqueados=[seat.id_asiento for seat in locked_seats],
        estado="Reservado",
    )


def publish_current_seat_map(db: Session, showtime_id: int) -> None:
    """Envía la vista actualizada del mapa de asientos a los clientes conectados."""

    try:
        seat_map = get_showtime_seat_map(db, showtime_id)
        payload = {"type": "seat_map_update", "data": seat_map.model_dump()}
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(publish_showtime_update(showtime_id, payload))
        else:
            loop.create_task(publish_showtime_update(showtime_id, payload))
    except Exception:
        # La notificación no debe romper la compra si la capa websocket falla.
        return
