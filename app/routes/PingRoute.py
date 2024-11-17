from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from controller.PingController import db_ping_test


router = APIRouter(prefix="/ping")

@router.get("/db")
def ping_db_test(db: Session = Depends(get_db)):
    return db_ping_test(db=db)
