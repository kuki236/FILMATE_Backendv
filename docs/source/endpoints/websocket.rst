WebSocket de asientos (sincronización)
====================================

Endpoint WebSocket para sincronizar el mapa de asientos en tiempo real.

Conexión
--------

URL de conexión (ejemplo):

.. code-block:: http

   ws://<host>/ws/seats/{showtime_id}

Comportamiento:

- Al conectar, el servidor envía el estado actual del mapa de asientos (`seat_map`).
- Tras cambios (bloqueo/compra), el servidor emite eventos con el nuevo `seat_map`.

Ejemplo de payload emitido (JSON):

.. code-block:: http

   {
     "event": "seat_map",
     "showtime_id": 10,
     "seats": [{"id":1,"state":"reserved"},{"id":2,"state":"available"}]
   }
