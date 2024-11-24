from models.Usuario import Usuario
from models.UsuarioSesion import UsuarioSesion

from models.Pasajero import Pasajero

from models.Conductor import Conductor
from models.ConductorEmpresa import ConductorEmpresa
from models.ConductorPrivado import ConductorPrivado

from models.Marca import Marca
from models.Modelo import Modelo
from models.Color import Color

from models.Empresa import Empresa
from models.Empleado import Empleado

from models.Vehiculo import Vehiculo
from models.Transporte import Transporte
from models.Unidad import Unidad

from models.Ruta import Ruta
from models.Tarifa import Tarifa
from models.TarifaRuta import TarifaRuta


from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse


def db_ping_test(db: Session):
    return JSONResponse(content={"state": "success"}, status_code=200)