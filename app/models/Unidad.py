from sqlalchemy import Column, String, ForeignKey, INTEGER
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID

class Unidad(Base):
    __tablename__ = "unidad"

    id_unidad = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    id_propietario = Column(UUID(as_uuid=True), nullable=False) # puede ser una emmpresa o un conductor privado
    tipo_propietario = Column(String(1), nullable=False) # E: empresa , P: privado
    numero = Column(INTEGER, nullable=False)
    id_vehiculo = Column(UUID(as_uuid=True), ForeignKey('vehiculo.id_vehiculo'), nullable=False)
    id_transporte = Column(INTEGER, ForeignKey('transporte.id_transporte'), nullable=False)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)