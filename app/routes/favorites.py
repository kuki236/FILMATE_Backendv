from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.models.favorite import Favorito
from app.models.movie import Pelicula
from app.schemas.favorite import FavoriteResponse

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/", response_model=List[FavoriteResponse])
def list_favorites(user_id: int = Query(...), db: Session = Depends(get_db)):
    return (
        db.query(Favorito)
        .filter(Favorito.id_usuario == user_id)
        .order_by(Favorito.fecha_agregado.desc())
        .all()
    )


@router.post("/", response_model=FavoriteResponse, status_code=201)
def add_favorite(user_id: int = Query(...), movie_id: int = Query(...), db: Session = Depends(get_db)):
    movie = db.query(Pelicula).filter(Pelicula.id_pelicula == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    existing = db.query(Favorito).filter(
        Favorito.id_usuario == user_id,
        Favorito.id_pelicula == movie_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Movie already in favorites")

    fav = Favorito(id_usuario=user_id, id_pelicula=movie_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


@router.delete("/{movie_id}")
def remove_favorite(movie_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    fav = db.query(Favorito).filter(
        Favorito.id_usuario == user_id,
        Favorito.id_pelicula == movie_id
    ).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(fav)
    db.commit()
    return {"message": "Favorite removed"}
