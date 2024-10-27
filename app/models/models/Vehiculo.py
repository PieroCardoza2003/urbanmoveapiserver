from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Vehiculo(Base):
    __tablename__ = "vehiculo"

    id_vehiculo = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    placa = Column(String(10), nullable=True)
    marca = Column(String(20), nullable=False)
    modelo = Column(String(20), nullable=True)
    color = Column(String(20), nullable=False)

Base.metadata.create_all(engine)