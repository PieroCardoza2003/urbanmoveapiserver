from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class ConductorPrivado(Base):
    __tablename__ = "conductorprivado"

    id_conductorprivado = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_conductor = Column(UUID(as_uuid=True), ForeignKey('conductor.id_conductor'), nullable=False)
    id_unidad = Column(UUID(as_uuid=True), ForeignKey('unidad.id_unidad'), nullable=False)
    numero_licencia = Column(String(20), nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    foto_licencia_frontal = Column(String, nullable=False)
    foto_licencia_reverso = Column(String, nullable=False)

Base.metadata.create_all(engine)