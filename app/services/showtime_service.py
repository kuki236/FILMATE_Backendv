"""Servicios para consulta de funciones y horarios por sede."""

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cinema import Cine
from app.models.movie import Pelicula
from app.models.room import Sala
from app.models.seat import Asiento
from app.models.showtime import Funcion
from app.models.showtime_seat import FuncionAsiento
from app.schemas.showtime import CinemaShowtimesResponse, ShowtimeAvailabilityItem


def list_showtimes_by_cinema(db: Session, cinema_id: int, only_future: bool = True) -> CinemaShowtimesResponse:
    """Devuelve las funciones disponibles de una sede con totales de asientos."""

    cinema = db.get(Cine, cinema_id)
    if not cinema:
        raise HTTPException(status_code=404, detail="Cine no encontrado")

    stmt = (
        select(Funcion, Pelicula, Sala)
        .join(Pelicula, Funcion.id_pelicula == Pelicula.id_pelicula)
        .join(Sala, Funcion.id_sala == Sala.id_sala)
        .where(Sala.id_cine == cinema_id)
    )

    if only_future:
        stmt = stmt.where(Funcion.fecha_hora_inicio >= datetime.utcnow())

    rows = db.execute(stmt.order_by(Funcion.fecha_hora_inicio)).all()
    funciones = []

    for funcion, pelicula, sala in rows:
        asientos_totales = db.scalar(
            select(func.count(Asiento.id_asiento)).where(Asiento.id_sala == sala.id_sala)
        ) or 0

        asientos_bloqueados = db.scalar(
            select(func.count(FuncionAsiento.id_asiento)).where(
                FuncionAsiento.id_funcion == funcion.id_funcion,
                FuncionAsiento.estado.in_(["Reservado", "Vendido"]),
            )
        ) or 0

        funciones.append(
            ShowtimeAvailabilityItem(
                id_funcion=funcion.id_funcion,
                id_pelicula=pelicula.id_pelicula,
                titulo_pelicula=pelicula.titulo,
                id_sala=sala.id_sala,
                nombre_sala=sala.nombre,
                fecha_hora_inicio=funcion.fecha_hora_inicio,
                fecha_hora_fin=funcion.fecha_hora_fin,
                idioma=funcion.idioma,
                formato=funcion.formato,
                asientos_totales=asientos_totales,
                asientos_disponibles=max(asientos_totales - asientos_bloqueados, 0),
            )
        )

    return CinemaShowtimesResponse(
        id_cine=cinema.id_cine,
        nombre_cine=cinema.nombre,
        ciudad=cinema.ciudad,
        funciones=funciones,
    )


def list_showtimes_by_movie(db: Session, movie_id: int):
    """Obtiene todas las funciones de una película."""

    showtimes = (
        db.query(Funcion)
        .filter(Funcion.id_pelicula == movie_id)
        .all()
    )

    if not showtimes:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron funciones para esta película"
        )

    return showtimes