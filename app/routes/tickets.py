"""Rutas para consultar el ticket final y reconstruir el payload QR."""

import logging
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.order import CheckoutRequest, CheckoutResponse
from app.schemas.ticket import TicketIssueResponse
from app.services.order_service import checkout_purchase, get_ticket_bundle_for_reservation
from app.utils.ticket_pdf import build_ticket_pdf

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/issue", response_model=CheckoutResponse)
def issue_ticket(payload: CheckoutRequest, db: Session = Depends(get_db)):
    """Atajo para cerrar compra y emitir el ticket final."""

    logger.info("📥 POST /tickets/issue - usuario=%s función=%s", payload.id_usuario, payload.id_funcion)
    try:
        return checkout_purchase(db, payload)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("❌ Error en POST /tickets/issue: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/reservation/{reservation_id}", response_model=TicketIssueResponse)
def get_ticket_payload(reservation_id: int, db: Session = Depends(get_db)):
    """Recupera el JSON final utilizado para el QR de una reserva."""

    logger.info("📥 GET /tickets/reservation/%s", reservation_id)
    try:
        return get_ticket_bundle_for_reservation(db, reservation_id)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("❌ Error en GET /tickets/reservation/%s: %s", reservation_id, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/reservation/{reservation_id}/pdf")
def download_ticket_pdf(reservation_id: int, db: Session = Depends(get_db)):
    """Genera y descarga el ticket definitivo en PDF."""

    logger.info("📥 GET /tickets/reservation/%s/pdf", reservation_id)
    try:
        bundle = get_ticket_bundle_for_reservation(db, reservation_id)
        pdf_bytes = build_ticket_pdf(bundle)
        filename = f"ticket_reserva_{reservation_id}.pdf"
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("❌ Error en GET /tickets/reservation/%s/pdf: %s", reservation_id, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
