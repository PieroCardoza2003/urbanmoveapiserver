from sqlalchemy import Column, String, Integer, ForeignKey
from database.db import Base, engine

class Modelo(Base):
    __tablename__ = "modelo"

    id_modelo = Column(Integer, primary_key=True, autoincrement=True)
    id_marca = Column(Integer, ForeignKey('marca.id_marca'), nullable=False)
    modelo = Column(String(20), nullable=False)

Base.metadata.create_all(engine)