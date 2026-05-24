Asientos (mapa y bloqueo)
==========================

Endpoints para obtener el mapa de asientos y bloquear asientos transaccionalmente.

Obtener mapa de asientos
-------------------------

.. code-block:: http

   GET /seats/showtime/{showtime_id} HTTP/1.1

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json

   {
     "showtime_id": 10,
     "seats": [
       {"id": 1, "row": "A", "number": 1, "state": "available"},
       {"id": 2, "row": "A", "number": 2, "state": "reserved"}
     ]
   }

Bloqueo transaccional
----------------------

.. code-block:: http

   POST /seats/lock HTTP/1.1
   Content-Type: application/json

   {
     "id_usuario": 42,
     "id_funcion": 10,
     "ids_asientos": [1,2]
   }

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json

   {"locked": [1,2], "status": "ok"}

Notas:

- El bloqueo se realiza dentro de una transacción con `FOR UPDATE` para evitar dobles ventas.
- Al confirmar la compra se genera la reserva y los boletos.
