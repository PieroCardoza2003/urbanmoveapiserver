from sqlalchemy import Column, String, Date, Integer, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.uuid_utils import get_uuid

class Conductor(Base):
    __tablename__ = "conductor"

    id_conductor = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey('usuario.id_usuario'), nullable=False)
    tipo_conductor = Column(String(20), nullable=False) # EMPRESA - PRIVADO
    puntuacion = Column(Integer, nullable=True, default=0)
    alcance_busqueda = Column(String(10), nullable=True, default="500.0")
    numero_licencia = Column(String(15), nullable=False) # Peru 9
    fecha_vencimiento = Column(Date, nullable=False) #YYYY-MM-DD
    licencia_frontal = Column(String, nullable=False)
    licencia_reverso = Column(String, nullable=False)

    # agregar relaciones con sus respectivas tablas
    id_unidad = Column(Integer, nullable=True)
    id_ruta = Column(Integer, nullable=True)

Base.metadata.create_all(engine)