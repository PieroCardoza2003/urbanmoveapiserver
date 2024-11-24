from sqlalchemy import Column, String, INTEGER
from database.db import Base, engine

class Tarifa(Base):
    __tablename__ = "tarifa"

    id_tarifa = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(15), nullable=False)

Base.metadata.create_all(engine)