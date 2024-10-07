from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base, engine
from utils.uuid_utils import get_uuid


class UsuarioSesion(Base):
    __tablename__ = "usuario_sesion"

    id_sesion = Column(UUID(as_uuid=True), primary_key=True, index=True, default=get_uuid)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey('usuario.id_usuario'), nullable=False, unique=True)
    ip_usuario = Column(String(30), nullable=True)
    token = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_expiracion = Column(DateTime, nullable=False)

Base.metadata.create_all(engine)