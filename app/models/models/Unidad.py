from sqlalchemy import Column, String, Date, DateTime, ForeignKey, INTEGER
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Unidad(Base):
    __tablename__ = "unidad"

    id_unidad = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_empresa = Column(UUID(as_uuid=True), ForeignKey('empresa.id_empresa'), nullable=False)
    id_vehiculo = Column(UUID(as_uuid=True), ForeignKey('vehiculo.id_vehiculo'), nullable=False)
    id_transporte = Column(UUID(as_uuid=True), ForeignKey('transporte.id_transporte'), nullable=False)
    id_propietario = Column(UUID(as_uuid=True), nullable=False)
    tipo_propietario = Column(String(1), nullable=False)
    numero = Column(INTEGER, nullable=False)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)