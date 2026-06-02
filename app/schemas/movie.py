from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.banner import BannerHome


class MovieBase(BaseModel):
    titulo: str
    sinopsis: Optional[str] = None
    duracion_minutos: Optional[int] = None
    clasificacion_edad: Optional[str] = None
    url_poster: Optional[str] = None
    url_trailer: Optional[str] = None


class MovieCreate(BaseModel):

    titulo: str
    sinopsis: str | None = None
    duracion_minutos: int | None = None
    clasificacion_edad: str | None = None

    url_poster: str | None = None
    url_trailer: str | None = None
    url_banner: str | None = None

    categoria_cartelera: str
    estado_registro: str

    generos: list[int]

    elenco: list[dict] = []

    directores: list[int] = []

class ActorInput(BaseModel):
    nombre: str
    personaje: str

class MovieUpdate(BaseModel):

    titulo: Optional[str] = None
    sinopsis: Optional[str] = None
    duracion_minutos: Optional[int] = None
    clasificacion_edad: Optional[str] = None

    categoria_cartelera: Optional[str] = None
    estado_registro: Optional[str] = None

    url_poster: Optional[str] = None
    url_banner: Optional[str] = None
    url_trailer: Optional[str] = None

    generos: List[int]

    elenco: List[ActorInput] = []

    directores: List[int] = []




class GeneroSchema(BaseModel):
    id_genero: int
    nombre: str
    class Config:
        from_attributes = True

class MovieResponse(MovieBase):
    id_pelicula: int
    categoria_cartelera: str
    estado_registro: str
    fecha_creacion: datetime
    generos: List[GeneroSchema] = []

    class Config:
        from_attributes = True

class MovieActorItem(BaseModel):
    nombre: str
    personaje: Optional[str] = None


class MovieGenreItem(BaseModel):
    nombre: str


class MovieDirectorItem(BaseModel):
    id_director: int
    nombre: str


class MovieDetailsResponse(BaseModel):
    id_pelicula: int
    titulo: str
    sinopsis: Optional[str] = None
    duracion_minutos: int
    clasificacion_edad: Optional[str] = None

    url_poster: Optional[str] = None
    url_trailer: Optional[str] = None
    url_banner: Optional[str] = None

    categoria_cartelera: Optional[str] = None

    generos: List[MovieGenreItem]
    actores: List[MovieActorItem]
    directores: List[MovieDirectorItem] = []

    promedio_resenas: float
    total_resenas: int