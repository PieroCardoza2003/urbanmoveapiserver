from sqlalchemy import Column, String, Integer
from database.db import Base, engine
from utils.uuid_utils import get_uuid

class Transporte(Base):
    __tablename__ = "transporte"

    id_transporte = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)

Base.metadata.create_all(engine)