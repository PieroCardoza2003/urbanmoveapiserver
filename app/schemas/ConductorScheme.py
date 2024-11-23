from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class ConductorEmpresaCreate(BaseModel):
    id_usuario: UUID

    nombre: str
    apellido: str
    fecha_nacimiento: date
    foto_perfil: Optional[str] = None

    numero_licencia: str
    fecha_vencimiento: date
    
    codigo_empleado: str

class ConductorPrivadoCreate(BaseModel):
    id_usuario: UUID

    nombre: str
    apellido: str
    fecha_nacimiento: date
    foto_perfil: Optional[str] = None

    numero_licencia: str
    fecha_vencimiento: date
    
    numero_placa: str
    marca_vehiculo: str
    modelo_vehiculo: str
    color_vehiculo: str