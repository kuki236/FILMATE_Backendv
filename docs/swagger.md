# Documentación API - Swagger UI

La API expone su documentación OpenAPI/Swagger de forma automática mediante FastAPI.

URLs disponibles en desarrollo:

- Swagger UI interactivo: `GET /docs`
- Redoc: `GET /redoc`
- Esquema OpenAPI JSON: `GET /openapi.json`

Cómo usar:

1. Levanta la aplicación:

```powershell
uvicorn app.main:app --reload
```

2. Abre en el navegador `http://localhost:8000/docs`.

3. Desde la UI de Swagger puedes: probar endpoints, ver esquemas de request/response, y copiar ejemplos de curl.

Notas adicionales:

- Asegúrate de tener la base de datos configurada y las variables de entorno antes de probar endpoints que persisten datos.
- Para añadir descripciones a endpoints o parámetros, edita las rutas en `app/routes/` y añade `summary` y `description` en los decoradores.
- Para documentar modelos complejos, completa los `schemas` en `app/schemas/`.

Generar archivo OpenAPI local (opcional):

Puedes volcar el JSON de OpenAPI a un archivo con una simple petición:

```powershell
curl http://localhost:8000/openapi.json -o openapi.json
```

Esto es útil para importar la especificación en herramientas externas (Postman, SwaggerHub, etc.).
