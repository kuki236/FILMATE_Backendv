from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.promotion import Promocion


def list_promotions(db: Session) -> List[Promocion]:
    return db.query(Promocion).order_by(Promocion.id_promocion.desc()).all()


def get_promotion(db: Session, promotion_id: int) -> Optional[Promocion]:
    return db.query(Promocion).filter(Promocion.id_promocion == promotion_id).first()


def get_promotion_by_code(db: Session, codigo: str) -> Optional[Promocion]:
    return db.query(Promocion).filter(Promocion.codigo_cupon == codigo).first()


def create_promotion(
    db: Session,
    codigo_cupon: str,
    porcentaje_descuento: Optional[float] = None,
    monto_descuento: Optional[float] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    limite_usos: Optional[int] = None,
) -> Promocion:
    promo = Promocion(
        codigo_cupon=codigo_cupon,
        porcentaje_descuento=porcentaje_descuento,
        monto_descuento=monto_descuento,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        limite_usos=limite_usos,
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo


def update_promotion(db: Session, promotion_id: int, data: dict) -> Optional[Promocion]:
    promo = get_promotion(db, promotion_id)
    if not promo:
        return None
    for key, value in data.items():
        if value is not None and hasattr(promo, key):
            setattr(promo, key, value)
    db.commit()
    db.refresh(promo)
    return promo


def delete_promotion(db: Session, promotion_id: int) -> bool:
    promo = get_promotion(db, promotion_id)
    if not promo:
        return False
    db.delete(promo)
    db.commit()
    return True


def validate_coupon(db: Session, codigo: str) -> Optional[dict]:
    promo = get_promotion_by_code(db, codigo)
    if not promo:
        return None

    now = datetime.now()
    if promo.fecha_inicio and now < promo.fecha_inicio:
        return {"valido": False, "motivo": "Cupón aún no vigente"}
    if promo.fecha_fin and now > promo.fecha_fin:
        return {"valido": False, "motivo": "Cupón expirado"}

    return {
        "valido": True,
        "id_promocion": promo.id_promocion,
        "codigo_cupon": promo.codigo_cupon,
        "porcentaje_descuento": float(promo.porcentaje_descuento) if promo.porcentaje_descuento else None,
        "monto_descuento": float(promo.monto_descuento) if promo.monto_descuento else None,
    }
