from sqlalchemy import Column, String, Date, DateTime, ForeignKey, INTEGER
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Viaje(Base):
    __tablename__ = "viaje"

    id_viaje = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_conductor = Column(UUID(as_uuid=True), ForeignKey('conductor.id_conductor'), nullable=False)
    id_unidad = Column(UUID(as_uuid=True), ForeignKey('unidad.id_unidad'), nullable=False)
    id_ruta = Column(UUID(as_uuid=True), ForeignKey('ruta.id_ruta'), nullable=False)
    fecha_viaje = Column(DateTime, nullable=False, default=get_datetime_now)

Base.metadata.create_all(engine)