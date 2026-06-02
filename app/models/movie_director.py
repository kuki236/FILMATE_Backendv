from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class PeliculaDirector(Base):
    __tablename__ = "pelicula_director"

    id_pelicula = Column(Integer, ForeignKey("pelicula.id_pelicula"), primary_key=True)
    id_director = Column(Integer, ForeignKey("director.id_director"), primary_key=True)

    pelicula = relationship("Pelicula", back_populates="directores")
    director = relationship("Director", back_populates="peliculas")
