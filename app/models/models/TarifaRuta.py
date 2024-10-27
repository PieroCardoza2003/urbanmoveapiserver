from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey, DECIMAL
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class TarifaRuta(Base):
    __tablename__ = "tarifaruta"

    id_ruta = Column(UUID(as_uuid=True), ForeignKey('ruta.id_ruta'), nullable=False)
    id_tarifa = Column(UUID(as_uuid=True), ForeignKey('tarifa.id_tarifa'), nullable=False)
    precio = Column(DECIMAL, nullable=False)

Base.metadata.create_all(engine)