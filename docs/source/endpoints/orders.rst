Checkout y órdenes
===================

Endpoint principal para finalizar compra y crear reserva/boletos.

.. code-block:: http

   POST /orders/checkout HTTP/1.1
   Content-Type: application/json

   {
     "id_usuario": 42,
     "id_funcion": 10,
     "ids_asientos": [1,2],
     "id_tarifa": 1,
     "productos_snack": [{"id_producto": 5, "cantidad": 2}]
   }

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 201 Created
   Content-Type: application/json

   {"reservation_id": 123, "tickets": [{"id": 987, "qr": "..."}]}

Notas:

- La operación es transaccional: bloquea asientos, crea la reserva, guarda snacks y emite los boletos.
- Después del checkout se publica el nuevo estado de asientos a través del WebSocket.
