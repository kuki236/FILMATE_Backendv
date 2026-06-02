from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.schemas.tariff import TariffCreate, TariffResponse
from app.repositories import tariff_repository

router = APIRouter(prefix="/tariffs", tags=["tariffs"])


@router.get("/", response_model=List[TariffResponse])
def list_tariffs(db: Session = Depends(get_db)):
    return tariff_repository.list_tariffs(db)


@router.get("/{tariff_id}", response_model=TariffResponse)
def get_tariff(tariff_id: int, db: Session = Depends(get_db)):
    tariff = tariff_repository.get_tariff(db, tariff_id)
    if not tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return tariff


@router.post("/", response_model=TariffResponse, status_code=201)
def create_tariff(payload: TariffCreate, db: Session = Depends(get_db)):
    return tariff_repository.create_tariff(db, payload.nombre, payload.precio, payload.dia_aplica)


@router.put("/{tariff_id}", response_model=TariffResponse)
def update_tariff(tariff_id: int, payload: TariffCreate, db: Session = Depends(get_db)):
    tariff = tariff_repository.update_tariff(db, tariff_id, payload.nombre, payload.precio, payload.dia_aplica)
    if not tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return tariff


@router.delete("/{tariff_id}")
def delete_tariff(tariff_id: int, db: Session = Depends(get_db)):
    deleted = tariff_repository.delete_tariff(db, tariff_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return {"message": "Tariff deleted"}
