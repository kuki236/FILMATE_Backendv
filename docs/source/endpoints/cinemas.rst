Cines
=====

Listado público de cines y datos básicos.

Obtener todos los cines
-----------------------

.. code-block:: http

   GET /cinemas HTTP/1.1

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json

   [
     {"id": 1, "nombre": "Cine Centro", "direccion": "Av. Falsa 123"},
     {"id": 2, "nombre": "Cine Norte", "direccion": "Calle 45"}
   ]
