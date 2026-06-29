from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    id_usuario: int
    id_pelicula: int
    puntuacion_estrellas: Optional[int] = None
    comentario: Optional[str] = None


class ReviewUpdate(BaseModel):
    puntuacion_estrellas: Optional[int] = None
    comentario: Optional[str] = None


class ReviewResponse(BaseModel):
    id_resena: int
    id_usuario: int
    id_pelicula: int
    puntuacion_estrellas: Optional[int] = None
    comentario: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ReviewWithUserResponse(BaseModel):
    id_resena: int
    id_usuario: int
    username: str
    url_perfil: Optional[str] = None
    puntuacion_estrellas: Optional[int] = None
    comentario: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    total_likes: int = 0
    liked_by_me: bool = False

    model_config = {"from_attributes": True}


class ToggleLikeRequest(BaseModel):
    id_usuario: int


class ReviewLikeResponse(BaseModel):
    id_resena: int
    total_likes: int
    liked_by_me: bool


class MovieMiniResponse(BaseModel):
    id_pelicula: int
    titulo: str
    url_poster: Optional[str] = None
    anio_lanzamiento: Optional[int] = None


class ReviewWithMovieResponse(BaseModel):
    id_resena: int
    id_usuario: int
    id_pelicula: int
    puntuacion_estrellas: Optional[int] = None
    comentario: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    total_likes: int = 0
    pelicula: MovieMiniResponse


class ReviewFeedItem(BaseModel):
    id_resena: int
    id_usuario: int
    username: str
    url_perfil: Optional[str] = None
    puntuacion_estrellas: Optional[int] = None
    comentario: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    total_likes: int = 0
    liked_by_me: bool = False
    pelicula: MovieMiniResponse
