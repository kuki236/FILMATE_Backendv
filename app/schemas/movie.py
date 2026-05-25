from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class MovieBase(BaseModel):
    titulo: str
    sinopsis: Optional[str] = None
    duracion_minutos: Optional[int] = None
    clasificacion_edad: Optional[str] = None
    url_poster: Optional[str] = None
    url_trailer: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    titulo: str
    sinopsis: str
    duracion_minutos: int
    clasificacion_edad: str
    url_poster: str
    url_trailer: str
    categoria_cartelera: str


class MovieResponse(MovieBase):
    id_pelicula: int
    categoria_cartelera: str
    estado_registro: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class MovieActorItem(BaseModel):
    nombre: str
    personaje: Optional[str] = None


class MovieGenreItem(BaseModel):
    nombre: str


class MovieDetailsResponse(BaseModel):
    id_pelicula: int
    titulo: str
    sinopsis: Optional[str] = None
    duracion_minutos: int
    clasificacion_edad: Optional[str] = None
    url_poster: Optional[str] = None
    url_trailer: Optional[str] = None
    categoria_cartelera: Optional[str] = None

    generos: List[MovieGenreItem]
    actores: List[MovieActorItem]

    promedio_resenas: float
    total_resenas: int