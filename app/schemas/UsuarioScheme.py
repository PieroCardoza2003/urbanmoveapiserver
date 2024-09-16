from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class UsuarioResponse(BaseModel):
    id_usuario: UUID
    nombres_usuario: str
    apellidos_usuario: Optional[str] = None
    fecha_nacimiento_usuario: Optional[date] = None
    foto_usuario: Optional[str] = None
    email_usuario: str
    password_usuario: str
    fecha_registro_usuario: datetime
    activo: str


class UsuarioCreate(BaseModel):
    nombres_usuario: str
    apellidos_usuario: Optional[str] = None
    fecha_nacimiento_usuario: Optional[date] = None
    email_usuario: str
    password_usuario: str