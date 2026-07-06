import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.log_actividad_sistema import LogActividadSistema
from app.repositories import notification_repository
from app.schemas.notification import (
    NotificacionCountResponse,
    NotificacionListResponse,
    NotificacionOut,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/notifications", tags=["admin notifications"])


@router.get("/", response_model=NotificacionListResponse)
def list_notificaciones(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[dict, Depends(get_current_admin)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = notification_repository.list_notificaciones(
        db, _admin["user_id"], page, limit
    )
    return NotificacionListResponse(
        data=[NotificacionOut.model_validate(n) for n in items],
        total=total,
        page=page,
        limit=limit,
    )


@router.get("/count", response_model=NotificacionCountResponse)
def count_notificaciones(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[dict, Depends(get_current_admin)],
):
    count = notification_repository.count_no_leidas(db, _admin["user_id"])
    return NotificacionCountResponse(count=count)


@router.put("/{id_notificacion}/read", response_model=NotificacionOut)
def marcar_leida(
    request: Request,
    id_notificacion: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[dict, Depends(get_current_admin)],
):
    notif = notification_repository.marcar_leida(
        db, id_notificacion, _admin["user_id"]
    )
    if not notif:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    db.add(LogActividadSistema(
        id_usuario=_admin.get("user_id"),
        accion_realizada=f"Notificación {id_notificacion} marcada como leída",
        modulo_afectado="NOTIFICACIONES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return NotificacionOut.model_validate(notif)


@router.put("/read-all")
def marcar_todas_leidas(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[dict, Depends(get_current_admin)],
):
    count = notification_repository.marcar_todas_leidas(db, _admin["user_id"])
    db.add(LogActividadSistema(
        id_usuario=_admin.get("user_id"),
        accion_realizada="Todas las notificaciones marcadas como leídas",
        modulo_afectado="NOTIFICACIONES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": f"{count} notificaciones marcadas como leídas"}
