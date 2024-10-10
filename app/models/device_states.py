from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DeviceState(Base):
    __tablename__ = "device_states"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, nullable=False)
