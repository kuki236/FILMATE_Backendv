"""Utilidades para construir el PDF final del ticket."""

from io import BytesIO

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.schemas.ticket import TicketIssueResponse


def build_ticket_pdf(bundle: TicketIssueResponse) -> bytes:
    """Genera un PDF en memoria con el resumen de la compra y el QR."""

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    qr_image = qrcode.make(bundle.qr.payload_json)
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_reader = ImageReader(qr_buffer)

    reserva = bundle.reserva
    boleto = bundle.boletos[0] if bundle.boletos else None
    qr = bundle.qr

    pdf.setTitle(f"Ticket Reserva {reserva.get('id_reserva')}")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(20 * mm, height - 25 * mm, "Filmate - Ticket Definitivo")

    pdf.setFont("Helvetica", 11)
    y = height - 40 * mm
    lines = [
        f"Reserva: {reserva.get('id_reserva')}",
        f"Usuario: {reserva.get('id_usuario')}",
        f"Funcion: {reserva.get('id_funcion')}",
        f"Estado pago: {reserva.get('estado_pago')}",
        f"Monto total: {reserva.get('monto_total')}",
        f"Metodo pago: {reserva.get('metodo_pago') or 'N/A'}",
        f"Transaccion: {reserva.get('transaccion_id') or 'N/A'}",
        f"QR version: {qr.version}",
    ]

    for line in lines:
        pdf.drawString(20 * mm, y, line)
        y -= 7 * mm

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(20 * mm, y - 2 * mm, "Boletos")
    y -= 10 * mm

    pdf.setFont("Helvetica", 10)
    for ticket in bundle.boletos:
        pdf.drawString(
            20 * mm,
            y,
            f"Boleto {ticket.id_boleto} | Asiento {ticket.id_asiento} | Codigo {ticket.codigo_qr}",
        )
        y -= 6 * mm

    if boleto is not None:
        pdf.drawString(20 * mm, y - 3 * mm, f"Primer boleto referencial: {boleto.codigo_qr}")

    pdf.drawImage(qr_reader, 130 * mm, height - 110 * mm, width=50 * mm, height=50 * mm)
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer.getvalue()
