from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class SolicitudRuta(Base):
    __tablename__ = "solicitudruta"

    id_solicittud = Column(UUID(as_uuid=True), ForeignKey('solicitud.id_solicitud'), nullable=False)
    id_ruta = Column(UUID(as_uuid=True), ForeignKey('ruta.id_ruta'), nullable=False)

Base.metadata.create_all(engine)