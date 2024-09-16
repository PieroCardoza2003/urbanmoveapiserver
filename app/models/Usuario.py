from sqlalchemy import Column, String, Date, DateTime
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    nombres_usuario = Column(String(80), nullable=False)
    apellidos_usuario = Column(String(80), nullable=True)
    fecha_nacimiento_usuario = Column(Date, nullable=True)
    foto_usuario = Column(String, nullable=True)
    email_usuario = Column(String(160), nullable=False, unique=True, index=True)
    password_usuario = Column(String, nullable=False)
    fecha_registro_usuario = Column(DateTime, nullable=False, default=get_datetime_now)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)