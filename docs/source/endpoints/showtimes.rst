Funciones y horarios
====================

Consultar funciones por cine.

.. code-block:: http

   GET /showtimes/cinema/{cinema_id} HTTP/1.1

Parámetros:

- `cinema_id`: id del cine.

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json

   [
     {"id": 10, "pelicula": {"id": 3, "titulo": "La Película"}, "hora_inicio": "2026-05-24T20:00:00"}
   ]
