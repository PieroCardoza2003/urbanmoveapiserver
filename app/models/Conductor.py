from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Conductor(Base):
    __tablename__ = "conductor"

    id_conductor = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey('usuario.id_usuario'), nullable=False)
    tipo_conductor = Column(String(20), nullable=False)
    puntuación = Column(Integer, nullable=True, default=0)
    alcance_busqueda = Column(String(10), nullable=True, default="500.0")
    id_unidad = Column(nullable=True)
    id_ruta = Column(nullable=True)

Base.metadata.create_all(engine)