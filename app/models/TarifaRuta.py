from sqlalchemy import Column, INTEGER, ForeignKey, DECIMAL
from database.db import Base, engine

class TarifaRuta(Base):
    __tablename__ = "tarifaruta"

    id_ruta = Column(INTEGER, ForeignKey('ruta.id_ruta'), primary_key=True, nullable=False)
    id_tarifa = Column(INTEGER, ForeignKey('tarifa.id_tarifa'), primary_key=True, nullable=False)
    precio = Column(DECIMAL, nullable=False)

Base.metadata.create_all(engine)