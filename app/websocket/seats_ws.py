"""WebSocket para sincronización en tiempo real del mapa de asientos."""

import asyncio
from typing import Dict, List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

router = APIRouter()


class SeatConnectionManager:
    """Administra las conexiones WebSocket por función."""

    def __init__(self) -> None:
        self.connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, showtime_id: int) -> None:
        await websocket.accept()
        self.connections.setdefault(showtime_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, showtime_id: int) -> None:
        connections = self.connections.get(showtime_id, [])
        if websocket in connections:
            connections.remove(websocket)
        if not connections and showtime_id in self.connections:
            self.connections.pop(showtime_id, None)

    async def broadcast(self, showtime_id: int, payload: dict) -> None:
        connections = list(self.connections.get(showtime_id, []))
        for websocket in connections:
            try:
                await websocket.send_json(payload)
            except Exception:
                self.disconnect(websocket, showtime_id)


manager = SeatConnectionManager()


async def publish_showtime_update(showtime_id: int, payload: dict) -> None:
    """Difunde un evento a todas las conexiones del showtime indicado."""

    await manager.broadcast(showtime_id, payload)


@router.websocket("/ws/seats/{showtime_id}")
async def seats_websocket(
    websocket: WebSocket,
    showtime_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Mantiene a los clientes sincronizados con cambios en tiempo real."""

    from app.services.seat_service import get_showtime_seat_map

    await manager.connect(websocket, showtime_id)
    try:
        initial_map = get_showtime_seat_map(db, showtime_id)
        await websocket.send_json({"type": "seat_map", "data": initial_map.model_dump()})

        while True:
            try:
                message = await websocket.receive_text()
            except WebSocketDisconnect:
                break

            if message.lower() == "refresh":
                current_map = get_showtime_seat_map(db, showtime_id)
                await websocket.send_json({"type": "seat_map", "data": current_map.model_dump()})
            else:
                await websocket.send_json({"type": "ack", "message": "connected"})
    finally:
        manager.disconnect(websocket, showtime_id)
