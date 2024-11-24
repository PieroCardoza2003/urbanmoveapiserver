from sqlalchemy import Column, String, INTEGER, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID

class Ruta(Base):
    __tablename__ = "ruta"

    id_ruta = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    id_empresa = Column(UUID(as_uuid=True), ForeignKey('empresa.id_empresa'), nullable=False)
    letra_ruta = Column(String(10), nullable=False)
    horario = Column(String(40), nullable=False)
    id_transporte = Column(INTEGER, ForeignKey('transporte.id_transporte'), nullable=False)
    activo = Column(String(1), nullable=False, default="A")

Base.metadata.create_all(engine)