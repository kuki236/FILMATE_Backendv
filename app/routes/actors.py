from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.schemas.actor import ActorCreate, ActorResponse
from app.repositories import actor_repository

router = APIRouter(prefix="/actors", tags=["actors"])


@router.get("/", response_model=List[ActorResponse])
def list_actors(db: Session = Depends(get_db)):
    return actor_repository.list_actors(db)


@router.get("/{actor_id}", response_model=ActorResponse)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = actor_repository.get_actor(db, actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor


@router.post("/", response_model=ActorResponse, status_code=201)
def create_actor(payload: ActorCreate, db: Session = Depends(get_db)):
    return actor_repository.create_actor(db, payload.nombre)


@router.put("/{actor_id}", response_model=ActorResponse)
def update_actor(actor_id: int, payload: ActorCreate, db: Session = Depends(get_db)):
    actor = actor_repository.update_actor(db, actor_id, payload.nombre)
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor


@router.delete("/{actor_id}")
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    deleted = actor_repository.delete_actor(db, actor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Actor not found")
    return {"message": "Actor deleted"}
