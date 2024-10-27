from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Ruta(Base):
    __tablename__ = "ruta"

    id_ruta = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_propietario = Column(UUID(as_uuid=True), nullable=False)
    tipo_propietario = Column(String(1), nullable=False)
    id_transporte = Column(UUID(as_uuid=True), ForeignKey('transporte.id_transporte'), nullable=False)
    letra_ruta = Column(String(5), nullable=False)
    horario = Column(String(40), nullable=False)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)