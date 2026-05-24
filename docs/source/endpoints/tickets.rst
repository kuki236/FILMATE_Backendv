Boletos y descarga PDF
======================

Generación de QR y descarga de PDF para los boletos.

Emitir/consultar boletos
------------------------

.. code-block:: http

   GET /tickets/reservation/{reservation_id} HTTP/1.1

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json

   [{"id": 987, "seat_id": 1, "qr": "base64-or-data-url"}]

Descargar PDF (ejemplo de uso):

.. code-block:: http

   GET /tickets/{ticket_id}/pdf HTTP/1.1

Esta ruta devuelve un `application/pdf` con el boleto y el QR incorporado.
