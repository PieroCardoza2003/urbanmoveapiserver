from sqlalchemy import Column, ForeignKey
from database.db import Base, engine
from sqlalchemy.dialects.postgresql import UUID
from utils.uuid_utils import get_uuid

class ConductorPrivado(Base):
    __tablename__ = "conductor_privado"

    id_conductor_privado = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_conductor = Column(UUID(as_uuid=True), ForeignKey('conductor.id_conductor'), nullable=False)

Base.metadata.create_all(engine)