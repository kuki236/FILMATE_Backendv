"""Servicios para consulta de funciones y horarios por sede."""

import logging
from collections import defaultdict
from datetime import date, datetime, time, timedelta

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.cinema import Cine
from app.models.movie import Pelicula
from app.models.room import Sala
from app.models.seat import Asiento
from app.models.showtime import Funcion
from app.models.showtime_seat import AsientoFuncion
from app.schemas.showtime import CinemaShowtimesResponse, ShowtimeAvailabilityItem

logger = logging.getLogger(__name__)


def _base_showtime_query(db: Session):
    return (
        db.query(Funcion, Pelicula, Sala, Cine)
        .join(Pelicula, Funcion.id_pelicula == Pelicula.id_pelicula)
        .join(Sala, Funcion.id_sala == Sala.id_sala)
        .join(Cine, Sala.id_cine == Cine.id_cine)
    )


def _batch_seat_counts(db: Session, rows: list[tuple]) -> dict:
    sala_ids = list({sala.id_sala for _, _, sala, _ in rows})
    funcion_ids = [funcion.id_funcion for funcion, _, _, _ in rows]

    totales = {}
    if sala_ids:
        totals_by_sala = (
            db.query(Asiento.id_sala, func.count(Asiento.id_asiento))
            .filter(Asiento.id_sala.in_(sala_ids), Asiento.eliminado == False)
            .group_by(Asiento.id_sala)
            .all()
        )
        totales = {sala_id: count for sala_id, count in totals_by_sala}

    ocupados = {}
    if funcion_ids:
        ocupados_by_funcion = (
            db.query(AsientoFuncion.id_funcion, func.count(AsientoFuncion.id_asiento))
            .filter(
                AsientoFuncion.id_funcion.in_(funcion_ids),
                AsientoFuncion.estado.in_(["Ocupado", "Bloqueado"]),
            )
            .group_by(AsientoFuncion.id_funcion)
            .all()
        )
        ocupados = {func_id: count for func_id, count in ocupados_by_funcion}

    return {"totales": totales, "ocupados": ocupados}


def _build_availability_items(db: Session, rows: list[tuple]) -> list[ShowtimeAvailabilityItem]:
    if not rows:
        return []

    counts = _batch_seat_counts(db, rows)
    totales = counts["totales"]
    ocupados = counts["ocupados"]

    items = []
    for funcion, pelicula, sala, cine in rows:
        asientos_totales = totales.get(sala.id_sala, 0)
        asientos_ocupados = ocupados.get(funcion.id_funcion, 0)

        items.append(ShowtimeAvailabilityItem(
            id_funcion=funcion.id_funcion,
            id_pelicula=pelicula.id_pelicula,
            titulo_pelicula=pelicula.titulo or "",
            id_sala=sala.id_sala,
            nombre_sala=sala.nombre_sala or "",
            tipo_sala=sala.tipo_sala or "",
            tipo_formato=sala.tipo_formato or "",
            id_cine=cine.id_cine,
            nombre_cine=cine.nombre_cine or "",
            fecha_hora=funcion.fecha_hora,
            precio_base=float(funcion.precio_base or 0),
            asientos_totales=asientos_totales,
            asientos_disponibles=max(asientos_totales - asientos_ocupados, 0),
        ))

    return items


def list_showtimes_by_cinema(db: Session, cinema_id: int, only_future: bool = True) -> CinemaShowtimesResponse:
    cinema = db.query(Cine).filter(Cine.id_cine == cinema_id, Cine.eliminado == False).first()
    if not cinema:
        raise HTTPException(status_code=404, detail="Cine no encontrado")

    query = _base_showtime_query(db).filter(Sala.id_cine == cinema_id)

    if only_future:
        query = query.filter(Funcion.fecha_hora >= datetime.now())

    rows = query.order_by(Funcion.fecha_hora).all()
    logger.info("Showtimes por cine %s: %d funciones encontradas", cinema_id, len(rows))
    funciones = _build_availability_items(db, rows)

    return CinemaShowtimesResponse(
        id_cine=cinema.id_cine,
        nombre_cine=cinema.nombre_cine,
        funciones=funciones,
    )


def list_showtimes_by_movie(db: Session, movie_id: int) -> list[ShowtimeAvailabilityItem]:
    rows = (
        _base_showtime_query(db)
        .filter(Funcion.id_pelicula == movie_id)
        .order_by(Funcion.fecha_hora)
        .all()
    )
    logger.info("Showtimes por pelicula %s: %d funciones encontradas", movie_id, len(rows))
    return _build_availability_items(db, rows)


def list_showtimes_by_date(
    db: Session,
    target_date: date,
    cinema_id: int | None = None,
    movie_id: int | None = None,
) -> list[ShowtimeAvailabilityItem]:
    day_start = datetime.combine(target_date, time.min)
    day_end = day_start + timedelta(days=1)

    query = _base_showtime_query(db).filter(
        Funcion.fecha_hora >= day_start,
        Funcion.fecha_hora < day_end,
    )

    if movie_id is not None:
        query = query.filter(Funcion.id_pelicula == movie_id)

    if cinema_id is not None:
        query = query.filter(Sala.id_cine == cinema_id)

    rows = query.order_by(Funcion.fecha_hora).all()
    logger.info("Showtimes por fecha %s: %d funciones encontradas", target_date.isoformat(), len(rows))
    return _build_availability_items(db, rows)
