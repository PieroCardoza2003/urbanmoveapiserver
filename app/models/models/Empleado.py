from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Empleado(Base):
    __tablename__ = "empleado"

    id_empleado = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_empresa = Column(UUID(as_uuid=True), ForeignKey('empresa.id_empresa'), nullable=False)
    id_conductorempresa = Column(UUID(as_uuid=True), ForeignKey('conductorempresa.id_conductorempresa'), nullable=True)
    codigo_empleado = Column(String(20), nullable=False)
    fecha_registro_empleado = Column(DateTime, nullable=False, default=get_datetime_now)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)