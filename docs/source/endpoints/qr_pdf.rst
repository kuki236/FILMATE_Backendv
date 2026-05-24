Estructura QR y PDF
====================

Estructura del payload QR generado para cada boleto y forma de usar la descarga PDF.

Payload QR (ejemplo):

.. code-block:: http

   {
     "ticket_id": 987,
     "reservation_id": 123,
     "user": {"id": 42, "email": "user@example.com"},
     "showtime": {"id":10, "movie":"La Película", "start": "2026-05-24T20:00:00"},
     "seat": {"row":"A","number":1}
   }

El PDF generado por el backend incluye:

- Información del usuario y reserva.
- Datos de la función y asiento.
- Código QR con el payload anterior.
