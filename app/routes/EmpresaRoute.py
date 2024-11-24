from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from middlewares.auth import verify_access_token
from fastapi import HTTPException
from database.db import get_db
from controller.EmpresaController import empresa_create, empleado_create, empleado_get_all, empresa_get_all, empresa_login, unidad_create, unidad_get_all, vehiculo_get_all, route_create, route_get_all
from schemas.EmpresaScheme import EmpresaCreate, EmpleadoCreate, EmpresaLogin, UnidadCreate, RutaCreate


router = APIRouter(prefix="/company")

@router.post("/register-company")
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    return empresa_create(db=db, empresa=empresa)

@router.post("/register-employe")
def create_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    return empleado_create(db=db, empleado=empleado)


@router.post("/register-route")
def create_route(route: RutaCreate, db: Session = Depends(get_db)):
    return route_create(db=db, route=route)

@router.get("/all-route")
def get_all_route(empresaID: str, db: Session = Depends(get_db)):
    return route_get_all(empresaID=empresaID, db=db)


@router.post("/register-unit")
def create_unidad(unidad: UnidadCreate, db: Session = Depends(get_db)):
    return unidad_create(db=db, unidad=unidad)

@router.get("/all-unit")
def get_all_unidad(empresaID: str, db: Session = Depends(get_db)):
    return unidad_get_all(empresaID=empresaID, db=db)

@router.get("/all-vehicle")
def get_all_vehicle(db: Session = Depends(get_db)):
    return vehiculo_get_all(db=db)


@router.get("/all-company")
def get_all_empresa(db: Session = Depends(get_db)):
    return empresa_get_all(db=db)

@router.get("/all-employe")
def get_all_empleado(empresaID: str, db: Session = Depends(get_db)):
    return empleado_get_all(empresaID=empresaID, db=db)

@router.post("/login")
def login_empresa(empresa: EmpresaLogin, db: Session = Depends(get_db)):    
    return empresa_login(db=db, empresa=empresa)