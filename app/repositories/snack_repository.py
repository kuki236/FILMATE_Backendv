from sqlalchemy.orm import Session

from app.models.snack_category import CategoriaSnack
from app.models.snack_product import ProductoSnack


def list_categories(db: Session):

    return (
        db.query(CategoriaSnack)
        .filter(CategoriaSnack.estado == True)
        .order_by(CategoriaSnack.orden_visual)
        .all()
    )


def list_products(db: Session):

    return (
        db.query(ProductoSnack)
        .filter(ProductoSnack.is_activo == True)
        .all()
    )


def get_product(
    db: Session,
    product_id: int
):

    return (
        db.query(ProductoSnack)
        .filter(
            ProductoSnack.id_producto == product_id
        )
        .first()
    )