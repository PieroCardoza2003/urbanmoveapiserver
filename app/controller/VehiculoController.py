from models.Marca import Marca
from models.Modelo import Modelo
from models.Color import Color

from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def marca_vehiculo_get_all(db: Session):
    return db.query(Marca).order_by(Marca.marca).all()


def model_vehicle_get_all(db: Session, id: int):
    return db.query(Modelo).filter_by(id_marca=id).order_by(Modelo.modelo).all()

def color_vehicle_get_all(db: Session):
    return db.query(Color).order_by(Color.color).all()