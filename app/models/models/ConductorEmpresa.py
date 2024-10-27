from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class ConductorEmpresa(Base):
    __tablename__ = "conductorempresa"

    id_conductorempresa = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_conductor = Column(UUID(as_uuid=True), ForeignKey('conductor.id_conductor'), nullable=False)
    codigo_empleado = Column(String(20), nullable=False)

Base.metadata.create_all(engine)