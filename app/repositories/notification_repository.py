from sqlalchemy import func, update
from sqlalchemy.orm import Session

from app.models.notificacion_admin import NotificacionAdmin


def list_notificaciones(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 20,
) -> tuple[list[NotificacionAdmin], int]:
    query = db.query(NotificacionAdmin).where(
        NotificacionAdmin.leida == False,
        (NotificacionAdmin.id_usuario_destino.is_(None))
        | (NotificacionAdmin.id_usuario_destino == user_id),
    )
    total = query.count()
    items = (
        query.order_by(NotificacionAdmin.fecha_creacion.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return items, total


def count_no_leidas(db: Session, user_id: int) -> int:
    return (
        db.query(func.count(NotificacionAdmin.id_notificacion))
        .where(
            NotificacionAdmin.leida == False,
            (NotificacionAdmin.id_usuario_destino.is_(None))
            | (NotificacionAdmin.id_usuario_destino == user_id),
        )
        .scalar()
        or 0
    )


def marcar_leida(db: Session, notif_id: int, user_id: int) -> NotificacionAdmin | None:
    notif = (
        db.query(NotificacionAdmin)
        .where(
            NotificacionAdmin.id_notificacion == notif_id,
            (NotificacionAdmin.id_usuario_destino.is_(None))
            | (NotificacionAdmin.id_usuario_destino == user_id),
        )
        .first()
    )
    if not notif:
        return None
    notif.leida = True
    db.commit()
    db.refresh(notif)
    return notif


def marcar_todas_leidas(db: Session, user_id: int) -> int:
    result = (
        db.execute(
            update(NotificacionAdmin)
            .where(
                NotificacionAdmin.leida == False,
                (NotificacionAdmin.id_usuario_destino.is_(None))
                | (NotificacionAdmin.id_usuario_destino == user_id),
            )
            .values(leida=True)
        )
    )
    db.commit()
    return result.rowcount
