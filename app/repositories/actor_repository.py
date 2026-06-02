from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.actor import Actor


def list_actors(db: Session) -> List[Actor]:
    return db.query(Actor).order_by(Actor.nombre).all()


def get_actor(db: Session, actor_id: int) -> Optional[Actor]:
    return db.query(Actor).filter(Actor.id_actor == actor_id).first()


def create_actor(db: Session, nombre: str) -> Actor:
    actor = Actor(nombre=nombre)
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor


def update_actor(db: Session, actor_id: int, nombre: str) -> Optional[Actor]:
    actor = get_actor(db, actor_id)
    if not actor:
        return None
    actor.nombre = nombre
    db.commit()
    db.refresh(actor)
    return actor


def delete_actor(db: Session, actor_id: int) -> bool:
    actor = get_actor(db, actor_id)
    if not actor:
        return False
    db.delete(actor)
    db.commit()
    return True
