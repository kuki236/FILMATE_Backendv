from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.director import Director


def list_directors(db: Session) -> List[Director]:
    return db.query(Director).order_by(Director.nombre).all()


def get_director(db: Session, director_id: int) -> Optional[Director]:
    return db.query(Director).filter(Director.id_director == director_id).first()


def create_director(db: Session, nombre: str) -> Director:
    director = Director(nombre=nombre)
    db.add(director)
    db.commit()
    db.refresh(director)
    return director


def update_director(db: Session, director_id: int, nombre: str) -> Optional[Director]:
    director = get_director(db, director_id)
    if not director:
        return None
    director.nombre = nombre
    db.commit()
    db.refresh(director)
    return director


def delete_director(db: Session, director_id: int) -> bool:
    director = get_director(db, director_id)
    if not director:
        return False
    db.delete(director)
    db.commit()
    return True
