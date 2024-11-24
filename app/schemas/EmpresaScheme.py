from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List
from typing import Optional
from uuid import UUID

class EmpresaCreate(BaseModel):
    razon_social: str
    ruc: str
    direccion: str
    telefono: Optional[str] = None
    email: str
    password: str


class EmpleadoCreate(BaseModel):
    id_empresa: UUID

class EmpleadoResponse(BaseModel):
    codigo_empleado: str
    conductor: Optional[str]
    fecha_registro: Optional[datetime]

class EmpresaLogin(BaseModel):
    email: str
    password: str

class UnidadCreate(BaseModel):
    placa: str
    marca: str
    modelo: str
    color: str
    id_propietario: UUID
    numero: int
    id_transporte: int


class Tarifa(BaseModel):
    id_tarifa: int
    precio: Decimal

class RutaCreate(BaseModel):
    id_empresa: UUID
    letra_ruta: str
    horario: str
    id_transporte: int
    tarifas: List[Tarifa]
