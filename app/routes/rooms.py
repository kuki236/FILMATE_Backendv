"""Rutas CRUD para salas."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db

from app.models.room import Sala

from app.schemas.room import (
    RoomCreate,
    RoomResponse,
    RoomUpdate
)

from app.repositories import room_repository

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)


@router.get("/", response_model=List[RoomResponse])
def list_rooms(db: Session = Depends(get_db)):

    logger.info("📥 GET /rooms")

    return room_repository.list_rooms(db)


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):

    logger.info("📥 GET /rooms/%s", room_id)

    room = room_repository.get_room(db, room_id)

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return room


@router.post("/", response_model=RoomResponse)
def create_room(
    payload: RoomCreate,
    db: Session = Depends(get_db)
):

    logger.info("📥 POST /rooms")

    room = Sala(**payload.model_dump())

    return room_repository.create_room(db, room)


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    payload: RoomUpdate,
    db: Session = Depends(get_db)
):

    logger.info("📥 PUT /rooms/%s", room_id)

    room = room_repository.get_room(db, room_id)

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(room, key, value)

    return room_repository.update_room(db, room)


@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db)
):

    logger.info("📥 DELETE /rooms/%s", room_id)

    room = room_repository.get_room(db, room_id)

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    room_repository.delete_room(db, room)

    return {
        "message": "Room deleted successfully"
    }