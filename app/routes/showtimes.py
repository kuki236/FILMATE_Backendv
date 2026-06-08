import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.showtime import CinemaShowtimesResponse
from app.services.showtime_service import list_showtimes_by_cinema, list_showtimes_by_movie

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/showtimes", tags=["showtimes"])


@router.get("/cinema/{cinema_id}", response_model=CinemaShowtimesResponse)
def get_showtimes_by_cinema(cinema_id: int, db: Session = Depends(get_db)):
    logger.info("GET /showtimes/cinema/%s", cinema_id)
    return list_showtimes_by_cinema(db, cinema_id)


@router.get("/movie/{movie_id}")
def get_showtimes_by_movie(movie_id: int, db: Session = Depends(get_db)):
    logger.info("GET /showtimes/movie/%s", movie_id)
    return list_showtimes_by_movie(db, movie_id)
