"""API principal de Filmate.

Este módulo define la instancia de `FastAPI`, registra las rutas principales
y expone endpoints básicos de salud y estado. Los `tags_metadata` se usan
para mejorar la documentación automática (OpenAPI / Swagger).
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import logging

from app.core.database import engine, Base
from app.models import *
from app.routes import auth, cinemas, movies, users, reviews, showtimes, seats, orders, tickets, admin_transactions, snacks, rooms, directors, reembolsos, admin_reembolsos, favorites, tariffs, promotions, actors, reservations, admin_reservas
from app.websocket.seats_ws import router as seats_ws_router
from app.routes import admin_transactions

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "users", "description": "Operaciones sobre usuarios (registro, consulta)."},
    {"name": "auth", "description": "Registro de nuevos usuarios y autenticación."},
    {"name": "cinemas", "description": "Listado de sedes/cines disponibles para el cliente."},
    {"name": "movies", "description": "Catálogo de películas: listado, creación y detalles."},
    {"name": "reviews", "description": "Gestión de reseñas: creación y listado por película."},
    {"name": "showtimes", "description": "Consulta de funciones y horarios por sede."},
    {"name": "seats", "description": "Mapa y bloqueo transaccional de asientos."},
    {"name": "orders", "description": "Cierre de compra y confirmación de reserva."},
    {"name": "tickets", "description": "Emisión y consulta del payload QR final."},
    {"name": "directors", "description": "CRUD de directores."},
    {"name": "reembolsos", "description": "Solicitudes de reembolso (cliente)."},
    {"name": "admin reembolsos", "description": "Gestión de reembolsos (admin)."},
    {"name": "favorites", "description": "Favoritos del usuario."},
    {"name": "tariffs", "description": "CRUD de tarifas (admin)."},
    {"name": "promotions", "description": "CRUD de promociones y validación de cupones."},
    {"name": "actors", "description": "CRUD de actores."},
    {"name": "reservations", "description": "Historial de reservas por usuario."},
    {"name": "admin reservas", "description": "Listado admin de reservas."},
]

app = FastAPI(
    title="Filmate API",
    version="0.1.0",
    description="API para la plataforma Filmate. Documentación disponible en Swagger UI.",
    openapi_tags=tags_metadata,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

#Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(cinemas.router)
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(showtimes.router)
app.include_router(seats.router)
app.include_router(orders.router)
app.include_router(tickets.router)
app.include_router(seats_ws_router)
app.include_router(admin_transactions.router)
app.include_router(snacks.router)
app.include_router(rooms.router)
app.include_router(admin_transactions.router)
app.include_router(directors.router)
app.include_router(reembolsos.router)
app.include_router(admin_reembolsos.router)
app.include_router(favorites.router)
app.include_router(tariffs.router)
app.include_router(promotions.router)
app.include_router(actors.router)
app.include_router(reservations.router)
app.include_router(admin_reservas.router)


@app.get("/", summary="Estado del servicio")
def root():
    """Endpoint raíz que devuelve un mensaje simple indicando que la API está activa.

    Se utiliza para comprobaciones rápidas y para proporcionar un punto de entrada
    legible en la documentación.
    """
    logger.info("✅ GET / - API activa")
    return {"message": "Filmate API funcionando"}


@app.get("/docs", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/api/docs")


@app.get("/redoc", include_in_schema=False)
def redoc_redirect():
    return RedirectResponse(url="/api/redoc")


@app.get("/health", summary="Health Check - Verifica conexión a BD", tags=["health"])
def health_check():
    """Endpoint para verificar si la API y la BD están funcionando."""
    logger.info("🏥 GET /health - Verificando estado")
    try:
        with engine.connect() as conn:
            logger.info("✅ Health check: BD conectada")
            return {
                "status": "healthy",
                "database": "connected"
            }
    except Exception as e:
        logger.error(f"❌ Health check falló: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }