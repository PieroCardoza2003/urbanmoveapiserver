from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from schemas.UsuarioScheme import UsuarioResponse, UsuarioCreate
from controller.UsuarioController import user_get_all, user_get_one, user_create


router = APIRouter(prefix="/user")

@router.get("/list/all", response_model=List[UsuarioResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user_get_all(db=db)

@router.get("/get/{id}")
def get_one_user(id, db: Session = Depends(get_db)):
    return user_get_one(db=db, id=id)

@router.post("/create")
def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    return user_create(db=db, user=user)



