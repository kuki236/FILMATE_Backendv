"""Servicios para crear el payload final del ticket y su QR."""

import json
from datetime import datetime
from typing import Any, Dict, List

from app.models.cinema import Cine
from app.models.reservation import Reserva
from app.models.room import Sala
from app.models.seat import Asiento
from app.models.showtime import Funcion
from app.models.ticket import Boleto
from app.schemas.ticket import TicketQrPayload, TicketResponse


def build_ticket_response(ticket: Boleto) -> TicketResponse:
    """Convierte un boleto ORM en el esquema de respuesta."""

    return TicketResponse(
        id_boleto=ticket.id_boleto,
        id_reserva=ticket.id_reserva,
        id_funcion=ticket.id_funcion,
        id_asiento=ticket.id_asiento,
        id_tarifa=ticket.id_tarifa,
        precio_pagado=float(ticket.precio_pagado),
        codigo_qr=ticket.codigo_qr,
        estado_ingreso=ticket.estado_ingreso,
    )


def build_ticket_qr_payload(
    reserva: Reserva,
    funcion: Funcion,
    asientos: List[Asiento],
    boletos: List[Boleto],
) -> TicketQrPayload:
    """Genera el JSON que se codificará en el QR final del boleto."""

    pelicula = funcion.pelicula
    sala = funcion.sala
    cine = sala.cine if sala else None

    reserva_data: Dict[str, Any] = {
        "id_reserva": reserva.id_reserva,
        "id_usuario": reserva.id_usuario,
        "id_funcion": reserva.id_funcion,
        "id_promocion": reserva.id_promocion,
        "fecha_reserva": reserva.fecha_reserva,
        "fecha_expiracion": reserva.fecha_expiracion,
        "monto_subtotal": float(reserva.monto_subtotal),
        "descuento_aplicado": float(reserva.descuento_aplicado),
        "monto_total": float(reserva.monto_total),
        "estado_pago": reserva.estado_pago,
        "metodo_pago": reserva.metodo_pago,
        "transaccion_id": reserva.transaccion_id,
    }

    boletos_data = []
    for ticket in boletos:
        asiento = next((item for item in asientos if item.id_asiento == ticket.id_asiento), None)
        boletos_data.append(
            {
                "id_boleto": ticket.id_boleto,
                "id_asiento": ticket.id_asiento,
                "fila": asiento.fila if asiento else None,
                "numero": asiento.numero if asiento else None,
                "codigo_qr": ticket.codigo_qr,
                "precio_pagado": float(ticket.precio_pagado),
                "estado_ingreso": ticket.estado_ingreso,
            }
        )

    payload = {
        "version": "1.0",
        "generado_en": datetime.utcnow(),
        "reserva": reserva_data,
        "cine": {
            "id_cine": cine.id_cine if cine else None,
            "nombre": cine.nombre if cine else None,
            "ciudad": cine.ciudad if cine else None,
        },
        "sala": {
            "id_sala": sala.id_sala if sala else None,
            "nombre": sala.nombre if sala else None,
        },
        "funcion": {
            "id_funcion": funcion.id_funcion,
            "fecha_hora_inicio": funcion.fecha_hora_inicio,
            "fecha_hora_fin": funcion.fecha_hora_fin,
            "idioma": funcion.idioma,
            "formato": funcion.formato,
        },
        "pelicula": {
            "id_pelicula": pelicula.id_pelicula if pelicula else None,
            "titulo": pelicula.titulo if pelicula else None,
        },
        "boletos": boletos_data,
    }

    return TicketQrPayload(
        version="1.0",
        generado_en=datetime.utcnow(),
        reserva=reserva_data,
        boletos=boletos_data,
        payload_json=json.dumps(payload, ensure_ascii=False, default=str),
    )
