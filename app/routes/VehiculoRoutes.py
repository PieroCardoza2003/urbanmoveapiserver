from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import HTTPException
from database.db import get_db
from controller.VehiculoController import marca_vehiculo_get_all, model_vehicle_get_all


router = APIRouter(prefix="/vehicle")


@router.get("/brands")
def get_all_marca_vehiculo(db: Session = Depends(get_db)):
    return marca_vehiculo_get_all(db=db)

@router.get("models/get/{id}")
def get_all_modelo_vehiculo(id, db: Session = Depends(get_db)):
    return model_vehicle_get_all(db=db, id=id)