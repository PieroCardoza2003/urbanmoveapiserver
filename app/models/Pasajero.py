from sqlalchemy import Column, String, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.uuid_utils import get_uuid

class Pasajero(Base):
    __tablename__ = "pasajero"

    id_pasajero = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey('usuario.id_usuario'), nullable=False, index=True)
    alcance_busqueda = Column(String(10), nullable=True, default="500.0")

Base.metadata.create_all(engine)