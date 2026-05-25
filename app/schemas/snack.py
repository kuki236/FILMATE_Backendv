from typing import List

from pydantic import BaseModel


class SnackCategoryResponse(BaseModel):
    id_categoria: int
    nombre: str

    class Config:
        from_attributes = True


class SnackProductResponse(BaseModel):
    id_producto: int
    nombre: str
    descripcion: str
    precio_actual: float
    url_imagen: str
    id_categoria: int

    class Config:
        from_attributes = True


class CartItem(BaseModel):
    id_producto: int
    cantidad: int


class CartCalculateRequest(BaseModel):
    items: List[CartItem]


class CartCalculateResponse(BaseModel):
    subtotal: float
    total: float