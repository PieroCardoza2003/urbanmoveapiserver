from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.datetime_utils import get_datetime_now
from utils.uuid_utils import get_uuid

class Tarifa(Base):
    __tablename__ = "tarifa"

    id_tarifa = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    nombre = Column(String(15), nullable=False)

Base.metadata.create_all(engine)