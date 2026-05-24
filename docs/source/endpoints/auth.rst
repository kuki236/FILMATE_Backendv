Autenticación
==============

Endpoints de autenticación (registro e inicio de sesión).

Registro
--------

.. code-block:: http

   POST /auth/register HTTP/1.1
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "secret123",
     "nombre": "Juan Perez"
   }

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 201 Created
   Content-Type: application/json

   {
     "id": 42,
     "email": "user@example.com",
     "nombre": "Juan Perez"
   }

Inicio de sesión
----------------

.. code-block:: http

   POST /auth/login HTTP/1.1
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "secret123"
   }

Respuesta (ejemplo):

.. code-block:: http

   HTTP/1.1 200 OK
   Content-Type: application/json

   {
     "access_token": "eyJ..",
     "token_type": "bearer",
     "user": {"id": 42, "email": "user@example.com"}
   }
