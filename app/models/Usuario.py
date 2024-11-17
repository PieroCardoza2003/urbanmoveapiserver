from sqlalchemy import Column, String, Date, DateTime
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import datetime_now
from utils.uuid_utils import get_uuid

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    nombres = Column(String(80), nullable=False)
    apellidos = Column(String(80), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True) #YYYY-MM-DD
    email = Column(String(160), nullable=False, unique=True, index=True)
    password = Column(String, nullable=True)
    foto_perfil = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    rol_actual = Column(String(20), nullable=False, default="PASAJERO")
    tipo_autenticacion = Column(String(20), nullable=False, default="LOCAL")
    fecha_registro = Column(DateTime, nullable=False, default=datetime_now)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)