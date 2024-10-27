from sqlalchemy import Column, String, Integer
from database.db import Base, engine

class Marca(Base):
    __tablename__ = "marca"

    id_marca = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(20), nullable=False)

Base.metadata.create_all(engine)