from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.sensor_data import SensorData

# Schema para los sensores
class SensorBase(BaseModel):
    sensor_name: str
    sensor_type: str
    location: Optional[str] = None
    unit: str
    is_active: bool = True

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    id: int
    created_at: datetime
    sensor_data: List[SensorData] = []  # Relación con los datos de sensor

    class Config:
        from_attributes = True