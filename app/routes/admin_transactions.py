import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db

from app.schemas.transaction import (
    TransactionItem,
    TransactionDetail
)

from app.repositories import transaction_repository

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin/transactions",
    tags=["admin-transactions"]
)


@router.get(
    "/",
    response_model=List[TransactionItem],
    responses={
        500: {
            "description": "Internal Server Error"
        }
    }
)
def list_transactions(
    db: Session = Depends(get_db)
):
    logger.info("📥 GET /admin/transactions")

    try:
        return transaction_repository.list_transactions(db)

    except Exception as e:
        logger.error(
            f"❌ Error GET /admin/transactions: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get(
    "/{reservation_id}",
    response_model=TransactionDetail,
    responses={
        404: {
            "description": "Transaction not found"
        },
        500: {
            "description": "Internal Server Error"
        }
    }
)
def get_transaction_detail(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    logger.info(
        f"📥 GET /admin/transactions/{reservation_id}"
    )

    try:
        transaction = (
            transaction_repository.get_transaction_detail(
                db,
                reservation_id
            )
        )

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return transaction

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"❌ Error GET /admin/transactions/{reservation_id}: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )