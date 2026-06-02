from pydantic import BaseModel


class DirectorBase(BaseModel):
    nombre: str


class DirectorCreate(DirectorBase):
    pass


class DirectorResponse(DirectorBase):
    id_director: int

    class Config:
        from_attributes = True
