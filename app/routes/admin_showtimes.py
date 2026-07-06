import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_permiso
from app.models.showtime import Funcion
from app.models.log_actividad_sistema import LogActividadSistema
from app.repositories import showtime_repository
from app.schemas.showtime import ShowtimeCreate, ShowtimeResponse, ShowtimeUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/showtimes", tags=["admin showtimes"])


@router.get("/", response_model=List[ShowtimeResponse])
def admin_list_showtimes(
    db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_FUNCIONES"))],
):
    return showtime_repository.list_showtimes(db)


@router.post("/", response_model=ShowtimeResponse, status_code=201)
def create_showtime(
    request: Request,
    payload: ShowtimeCreate, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_FUNCIONES"))],
):
    logger.info("POST /admin/showtimes/ - pelicula=%s sala=%s", payload.id_pelicula, payload.id_sala)
    funcion = Funcion(
        id_pelicula=payload.id_pelicula,
        id_sala=payload.id_sala,
        fecha_hora=payload.fecha_hora,
        precio_base=payload.precio_base,
    )
    result = showtime_repository.create_showtime(db, funcion)
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Función creada: ID {result.id_funcion}",
        modulo_afectado="FUNCIONES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return result


@router.put("/{showtime_id}", response_model=ShowtimeResponse, responses={404: {"description": "Función no encontrada"}})
def update_showtime(
    request: Request,
    showtime_id: int, payload: ShowtimeUpdate, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_FUNCIONES"))],
):
    data = payload.model_dump(exclude_unset=True)
    updated = showtime_repository.update_showtime(db, showtime_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Función editada: {showtime_id}",
        modulo_afectado="FUNCIONES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return updated


@router.delete("/{showtime_id}", responses={404: {"description": "Función no encontrada"}})
def delete_showtime(
    request: Request,
    showtime_id: int, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_FUNCIONES"))],
):
    deleted = showtime_repository.delete_showtime(db, showtime_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Función eliminada: {showtime_id}",
        modulo_afectado="FUNCIONES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": "Función eliminada"}
