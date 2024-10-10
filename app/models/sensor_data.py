from sqlalchemy import Column, Integer, Float, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# Modelo para la tabla 'sensor_data'
class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False, index=True)
    value = Column(Float, nullable=False)
    recorded_at = Column(TIMESTAMP, server_default=func.now(), index=True)

    # Relación muchos-a-uno con sensors
    sensor = relationship("Sensor", back_populates="sensor_data")