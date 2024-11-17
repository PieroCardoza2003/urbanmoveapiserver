from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from middlewares.auth import verify_access_token
from fastapi import HTTPException
from database.db import get_db
from controller.VehiculoController import marca_vehiculo_get_all, model_vehicle_get_all, color_vehicle_get_all


router = APIRouter(prefix="/vehicle")


@router.get("/brands")
def get_all_marca_vehiculo(db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token error")
    return marca_vehiculo_get_all(db=db)

@router.get("/models/get/{id}")
def get_all_modelo_vehiculo(id, db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token error")
    return model_vehicle_get_all(db=db, id=id)

@router.get("/colors")
def get_all_color_vehiculo(db: Session = Depends(get_db), payload: dict = Depends(verify_access_token)):
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token error")
    return color_vehicle_get_all(db=db)
