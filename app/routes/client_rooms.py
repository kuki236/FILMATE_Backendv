import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories import room_repository
from app.schemas.room import RoomResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/client/rooms", tags=["client rooms"])


@router.get("/", response_model=List[RoomResponse])
def list_rooms(db: Annotated[Session, Depends(get_db)]):
    return room_repository.list_rooms(db)


@router.get("/{room_id}", response_model=RoomResponse, responses={404: {"description": "Sala no encontrada"}})
def get_room(room_id: int, db: Annotated[Session, Depends(get_db)]):
    room = room_repository.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return room
