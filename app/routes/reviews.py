from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db
from app.schemas.review import ReviewCreate, ReviewModerate, ReviewResponse
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


@router.put("/{review_id}/moderate", response_model=ReviewResponse)
def moderate_review(review_id: int, payload: ReviewModerate, db: Session = Depends(get_db)):
    review = review_repository.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if payload.estado_moderacion not in ("Aprobado", "Pendiente", "Oculto"):
        raise HTTPException(status_code=400, detail="Estado inválido. Use: Aprobado, Pendiente, Oculto")
    review.estado_moderacion = payload.estado_moderacion
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = review_repository.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}
