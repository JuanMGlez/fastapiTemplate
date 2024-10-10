
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.db.base import Base

# Modelo para la tabla 'settings'
class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_name = Column(String(255), nullable=False, unique=True, index=True)  # Índice en config_name
    config_value = Column(String(255), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())