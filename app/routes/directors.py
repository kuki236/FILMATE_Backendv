from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.schemas.director import DirectorCreate, DirectorResponse
from app.repositories import director_repository

router = APIRouter(
    prefix="/directors",
    tags=["directors"]
)


@router.get("/", response_model=List[DirectorResponse])
def list_directors(db: Session = Depends(get_db)):
    return director_repository.list_directors(db)


@router.get("/{director_id}", response_model=DirectorResponse)
def get_director(director_id: int, db: Session = Depends(get_db)):
    director = director_repository.get_director(db, director_id)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director


@router.post("/", response_model=DirectorResponse, status_code=201)
def create_director(payload: DirectorCreate, db: Session = Depends(get_db)):
    return director_repository.create_director(db, payload.nombre)


@router.put("/{director_id}", response_model=DirectorResponse)
def update_director(director_id: int, payload: DirectorCreate, db: Session = Depends(get_db)):
    director = director_repository.update_director(db, director_id, payload.nombre)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director


@router.delete("/{director_id}")
def delete_director(director_id: int, db: Session = Depends(get_db)):
    deleted = director_repository.delete_director(db, director_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Director not found")
    return {"message": "Director deleted successfully"}
