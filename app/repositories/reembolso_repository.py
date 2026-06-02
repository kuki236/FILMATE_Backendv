from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.solicitud_reembolso import SolicitudReembolso
from app.models.motivo_devolucion import MotivoDevolucion


# =========================================
# MOTIVOS DE DEVOLUCIÓN
# =========================================

def list_motivos(db: Session) -> List[MotivoDevolucion]:
    return db.query(MotivoDevolucion).all()


def get_motivo(db: Session, motivo_id: int) -> Optional[MotivoDevolucion]:
    return db.query(MotivoDevolucion).filter(MotivoDevolucion.id_motivo == motivo_id).first()


def create_motivo(db: Session, descripcion: str) -> MotivoDevolucion:
    motivo = MotivoDevolucion(descripcion=descripcion)
    db.add(motivo)
    db.commit()
    db.refresh(motivo)
    return motivo


def update_motivo(db: Session, motivo_id: int, descripcion: str) -> Optional[MotivoDevolucion]:
    motivo = get_motivo(db, motivo_id)
    if not motivo:
        return None
    motivo.descripcion = descripcion
    db.commit()
    db.refresh(motivo)
    return motivo


def delete_motivo(db: Session, motivo_id: int) -> bool:
    motivo = get_motivo(db, motivo_id)
    if not motivo:
        return False
    db.delete(motivo)
    db.commit()
    return True


# =========================================
# SOLICITUDES DE REEMBOLSO
# =========================================

def create_solicitud(
    db: Session,
    id_reserva: int,
    id_motivo: int,
    monto_reembolsado: float,
    tipo_reembolso: str,
    detalle_motivo: Optional[str] = None,
) -> SolicitudReembolso:
    solicitud = SolicitudReembolso(
        id_reserva=id_reserva,
        id_motivo=id_motivo,
        monto_reembolsado=monto_reembolsado,
        tipo_reembolso=tipo_reembolso,
        detalle_motivo=detalle_motivo,
    )
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)
    return solicitud


def list_solicitudes_by_user(db: Session, id_usuario: int) -> List[SolicitudReembolso]:
    return (
        db.query(SolicitudReembolso)
        .options(
            joinedload(SolicitudReembolso.motivo),
            joinedload(SolicitudReembolso.reserva),
        )
        .join(SolicitudReembolso.reserva)
        .filter(SolicitudReembolso.reserva.has(id_usuario=id_usuario))
        .order_by(SolicitudReembolso.fecha_solicitud.desc())
        .all()
    )


def list_solicitudes_admin(
    db: Session,
    estado: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> List[SolicitudReembolso]:
    query = db.query(SolicitudReembolso).options(
        joinedload(SolicitudReembolso.motivo),
        joinedload(SolicitudReembolso.reserva),
        joinedload(SolicitudReembolso.administrador),
    )

    if estado:
        query = query.filter(SolicitudReembolso.estado_solicitud == estado)

    return query.order_by(SolicitudReembolso.fecha_solicitud.desc()).offset(skip).limit(limit).all()


def get_solicitud(db: Session, solicitud_id: int) -> Optional[SolicitudReembolso]:
    return (
        db.query(SolicitudReembolso)
        .options(
            joinedload(SolicitudReembolso.motivo),
            joinedload(SolicitudReembolso.reserva),
            joinedload(SolicitudReembolso.administrador),
        )
        .filter(SolicitudReembolso.id_solicitud == solicitud_id)
        .first()
    )


def resolve_solicitud(
    db: Session,
    solicitud_id: int,
    id_administrador: int,
    estado_solicitud: str,
    comentario_resolucion: Optional[str] = None,
) -> Optional[SolicitudReembolso]:
    solicitud = get_solicitud(db, solicitud_id)
    if not solicitud:
        return None

    solicitud.id_administrador = id_administrador
    solicitud.estado_solicitud = estado_solicitud
    solicitud.fecha_resolucion = datetime.now()
    if comentario_resolucion is not None:
        solicitud.comentario_resolucion = comentario_resolucion

    db.commit()
    db.refresh(solicitud)
    return solicitud


def count_solicitudes_by_estado(db: Session) -> dict:
    counts = (
        db.query(
            SolicitudReembolso.estado_solicitud,
            func.count(SolicitudReembolso.id_solicitud),
        )
        .group_by(SolicitudReembolso.estado_solicitud)
        .all()
    )

    total_monto = (
        db.query(func.coalesce(func.sum(SolicitudReembolso.monto_reembolsado), 0))
        .filter(SolicitudReembolso.estado_solicitud == "Aprobada")
        .scalar()
    )

    result = {"pendientes": 0, "aprobadas": 0, "rechazadas": 0, "monto_total_aprobado": float(total_monto)}
    for estado, count in counts:
        key = estado.lower() + "s"
        if key in result:
            result[key] = count
    return result
