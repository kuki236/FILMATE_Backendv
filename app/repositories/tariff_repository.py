from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.tariff import Tarifa


def list_tariffs(db: Session) -> List[Tarifa]:
    return db.query(Tarifa).all()


def get_tariff(db: Session, tariff_id: int) -> Optional[Tarifa]:
    return db.query(Tarifa).filter(Tarifa.id_tarifa == tariff_id).first()


def create_tariff(db: Session, nombre: str, precio: float, dia_aplica: str) -> Tarifa:
    tarifa = Tarifa(nombre=nombre, precio=precio, dia_aplica=dia_aplica)
    db.add(tarifa)
    db.commit()
    db.refresh(tarifa)
    return tarifa


def update_tariff(db: Session, tariff_id: int, nombre: str, precio: float, dia_aplica: str) -> Optional[Tarifa]:
    tarifa = get_tariff(db, tariff_id)
    if not tarifa:
        return None
    tarifa.nombre = nombre
    tarifa.precio = precio
    tarifa.dia_aplica = dia_aplica
    db.commit()
    db.refresh(tarifa)
    return tarifa


def delete_tariff(db: Session, tariff_id: int) -> bool:
    tarifa = get_tariff(db, tariff_id)
    if not tarifa:
        return False
    db.delete(tarifa)
    db.commit()
    return True
