from sqlalchemy.orm import Session
from app.models.seguidor import Seguidor
from app.models.historial_actividad import HistorialActividad
from typing import List


def follow(db: Session, id_seguidor: int, id_seguido: int) -> Seguidor:
    existing = (
        db.query(Seguidor)
        .filter(Seguidor.id_seguidor == id_seguidor, Seguidor.id_seguido == id_seguido)
        .first()
    )
    if existing:
        return existing
    s = Seguidor(id_seguidor=id_seguidor, id_seguido=id_seguido)
    db.add(s)
    # El trigger de BD ya registra el evento en el feed de quien sigue (SEGUIDOR);
    # esta fila avisa al usuario seguido, que de otra forma no se enteraría.
    db.add(
        HistorialActividad(
            id_usuario=id_seguido,
            tipo_evento="SEGUIDOR_RECIBIDO",
            id_referencia_usuario=id_seguidor,
            texto_breve="Tienes un nuevo seguidor.",
        )
    )
    db.commit()
    return s


def unfollow(db: Session, id_seguidor: int, id_seguido: int) -> bool:
    s = (
        db.query(Seguidor)
        .filter(Seguidor.id_seguidor == id_seguidor, Seguidor.id_seguido == id_seguido)
        .first()
    )
    if not s:
        return False
    db.delete(s)
    db.commit()
    return True


def list_followers(db: Session, user_id: int) -> List[Seguidor]:
    return db.query(Seguidor).filter(Seguidor.id_seguido == user_id).all()


def list_following(db: Session, user_id: int) -> List[Seguidor]:
    return db.query(Seguidor).filter(Seguidor.id_seguidor == user_id).all()


def is_following(db: Session, id_seguidor: int, id_seguido: int) -> bool:
    return (
        db.query(Seguidor)
        .filter(Seguidor.id_seguidor == id_seguidor, Seguidor.id_seguido == id_seguido)
        .first()
        is not None
    )


def count_followers(db: Session, user_id: int) -> int:
    return db.query(Seguidor).filter(Seguidor.id_seguido == user_id).count()


def count_following(db: Session, user_id: int) -> int:
    return db.query(Seguidor).filter(Seguidor.id_seguidor == user_id).count()
