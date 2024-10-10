# app/models/devices.py
from sqlalchemy import Column, Integer, String, Text
from app.db.postgres import Base

class DeviceState(Base):
    __tablename__ = "device_states"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, nullable=False)
    state = Column(String, nullable=False)
    description = Column(Text, nullable=True)
