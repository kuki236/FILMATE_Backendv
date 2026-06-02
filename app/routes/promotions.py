from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.dependencies import get_db
from app.schemas.promotion import PromotionCreate, PromotionResponse
from app.repositories import promotion_repository

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/", response_model=List[PromotionResponse])
def list_promotions(db: Session = Depends(get_db)):
    return promotion_repository.list_promotions(db)


@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promo = promotion_repository.get_promotion(db, promotion_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promo


@router.post("/", response_model=PromotionResponse, status_code=201)
def create_promotion(payload: PromotionCreate, db: Session = Depends(get_db)):
    return promotion_repository.create_promotion(
        db=db,
        codigo_cupon=payload.codigo_cupon,
        porcentaje_descuento=payload.porcentaje_descuento,
        monto_descuento=payload.monto_descuento,
        fecha_inicio=payload.fecha_inicio,
        fecha_fin=payload.fecha_fin,
        limite_usos=payload.limite_usos,
    )


@router.put("/{promotion_id}", response_model=PromotionResponse)
def update_promotion(promotion_id: int, payload: PromotionCreate, db: Session = Depends(get_db)):
    promo = promotion_repository.update_promotion(db, promotion_id, payload.dict(exclude_unset=True))
    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promo


@router.delete("/{promotion_id}")
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    deleted = promotion_repository.delete_promotion(db, promotion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return {"message": "Promotion deleted"}


@router.get("/validate/{codigo}")
def validate_coupon(codigo: str, db: Session = Depends(get_db)):
    result = promotion_repository.validate_coupon(db, codigo)
    if not result:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return result
