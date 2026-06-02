from pydantic import BaseModel


class MotivoDevolucionBase(BaseModel):
    descripcion: str


class MotivoDevolucionCreate(MotivoDevolucionBase):
    pass


class MotivoDevolucionResponse(MotivoDevolucionBase):
    id_motivo: int

    class Config:
        from_attributes = True
