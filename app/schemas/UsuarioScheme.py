from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class UsuarioResponsex(BaseModel):
    id_usuario: UUID
    nombres: str
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: str
    password: str
    foto_perfil: Optional[str] = None
    ciudad: Optional[str] = None
    rol_actual: str
    tipo_autenticacion: str
    fecha_registro_usuario: datetime
    activo: str


class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: str
    password: Optional[str] = None
    

class UsuarioLogin(BaseModel):
    email: str
    password: str

class GoogleLogin(BaseModel):
    token: str

class UsuarioId(BaseModel):
    id_usuario: UUID

class UsuarioFind(BaseModel):
    email: str
    type: str

class UsuarioPassword(BaseModel):
    email: str
    password: str

class UsuarioCode(BaseModel):
    email: str
    code: str

class UsuarioToken(BaseModel):
    token: str

class UsuarioResponse(BaseModel):
    id_usuario: UUID
    nombres: str
    apellidos: Optional[str] = None
    foto_perfil: Optional[str] = None