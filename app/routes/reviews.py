from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db
from app.schemas.review import ReviewCreate, ReviewResponse
from app.models.review import Resena
from app.repositories import review_repository

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    review = Resena(
        id_usuario=1,
        id_pelicula=payload.id_pelicula,
        calificacion_estrellas=payload.calificacion_estrellas,
        comentario=payload.comentario
    )

    created = review_repository.create_review(db, review)
    return created


@router.get("/movie/{movie_id}", response_model=List[ReviewResponse])
def list_reviews_for_movie(movie_id: int, db: Session = Depends(get_db)):
    return review_repository.list_reviews_for_movie(db, movie_id)
