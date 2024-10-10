from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema para sensor_data
class SensorDataBase(BaseModel):
    value: float

class SensorDataCreate(SensorDataBase):
    sensor_id: int  # Necesario para crear un dato de sensor

class SensorData(SensorDataBase):
    id: int
    sensor_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True

# Esquema para respuesta paginada
class PaginatedSensorData(BaseModel):
    total: int
    data: List[SensorData]
