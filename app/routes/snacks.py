import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.schemas.snack import (
    SnackCategoryResponse,
    SnackProductResponse,
    CartCalculateRequest,
    CartCalculateResponse
)

from app.repositories import snack_repository

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/snacks",
    tags=["snacks"]
)


@router.get(
    "/categories",
    response_model=list[SnackCategoryResponse]
)
def list_categories(
    db: Session = Depends(get_db)
):
    logger.info("📥 GET /snacks/categories")

    try:
        return snack_repository.list_categories(db)

    except Exception as e:
        logger.error(
            f"❌ Error GET /snacks/categories: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get(
    "/products",
    response_model=list[SnackProductResponse]
)
def list_products(
    db: Session = Depends(get_db)
):
    logger.info("📥 GET /snacks/products")

    try:
        return snack_repository.list_products(db)

    except Exception as e:
        logger.error(
            f"❌ Error GET /snacks/products: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post(
    "/cart/calculate",
    response_model=CartCalculateResponse
)
def calculate_cart(
    payload: CartCalculateRequest,
    db: Session = Depends(get_db)
):
    logger.info("📥 POST /snacks/cart/calculate")

    try:

        subtotal = 0

        for item in payload.items:

            product = snack_repository.get_product(
                db,
                item.id_producto
            )

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Producto {item.id_producto} no encontrado"
                )

            subtotal += (
                product.precio_actual * item.cantidad
            )

        return {
            "subtotal": subtotal,
            "total": subtotal
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"❌ Error POST /snacks/cart/calculate: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )