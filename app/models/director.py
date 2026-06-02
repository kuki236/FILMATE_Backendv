from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Director(Base):
    __tablename__ = "director"

    id_director = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)

    peliculas = relationship("PeliculaDirector", back_populates="director")
