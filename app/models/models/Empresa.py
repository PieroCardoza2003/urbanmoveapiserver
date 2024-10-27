from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Empresa(Base):
    __tablename__ = "empresa"

    id_empresa = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    razon_social = Column(String(80), nullable=False)
    ruc = Column(String(20), nullable=False)
    dirección = Column(String(80), nullable=False)
    telefono = Column(String(20), nullable=True)
    email_empresa = Column(String(160), nullable=False, unique=True, index=True)
    fecha_registro_empresa = Column(DateTime, nullable=False, default=get_datetime_now)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)