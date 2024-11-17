from sqlalchemy import Column, String, DateTime
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import datetime_now
from utils.uuid_utils import get_uuid

class Empresa(Base):
    __tablename__ = "empresa"

    id_empresa = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    razon_social = Column(String(80), nullable=False)
    ruc = Column(String(20), nullable=False)
    direccion = Column(String(80), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(160), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    fecha_registro_empresa = Column(DateTime, nullable=False, default=datetime_now)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)