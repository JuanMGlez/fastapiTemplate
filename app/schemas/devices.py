# app/schemas/devices.py
from pydantic import BaseModel

class DeviceStateCreate(BaseModel):
    device_id: int
    state: str
    description: str = None  # Campo opcional

class DeviceStateResponse(DeviceStateCreate):
    id: int  # Se agregará el ID de la base de datos

    class Config:
        from_attributes = True
