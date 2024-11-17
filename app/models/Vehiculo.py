from sqlalchemy import Column, String
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.uuid_utils import get_uuid

class Vehiculo(Base):
    __tablename__ = "vehiculo"

    id_vehiculo = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    placa = Column(String(10), unique=True, nullable=False)
    marca = Column(String(20), nullable=False)
    modelo = Column(String(20), nullable=False)
    color = Column(String(20), nullable=False)

Base.metadata.create_all(engine)