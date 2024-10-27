from sqlalchemy import Column, String, Integer
from database.db import Base, engine

class Color(Base):
    __tablename__ = "color"

    id_color = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String(20), nullable=False)
    code = Column(String(20), nullable=False)

Base.metadata.create_all(engine)