from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

# Modelo para la tabla 'sensors'
class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_name = Column(String(255), nullable=False, index=True)
    sensor_type = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True)
    unit = Column(String(50), nullable=False)
    is_active = Column(Boolean, server_default='true', index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relación uno-a-muchos con sensor_data
    sensor_data = relationship("SensorData", back_populates="sensor", cascade="all, delete-orphan")
