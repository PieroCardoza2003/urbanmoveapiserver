from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Solicitud(Base):
    __tablename__ = "solicitud"

    id_solicitud = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_pasajero = Column(UUID(as_uuid=True), ForeignKey('pasajero.id_pasajero'), nullable=False)
    ubicacion = Column(String(40), nullable=False)
    fecha_solicitud = Column(DateTime, nullable=False, default=get_datetime_now)

Base.metadata.create_all(engine)