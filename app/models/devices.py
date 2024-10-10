# app/models/devices.py
from sqlalchemy import Column, Integer, String, Text
from app.db.postgres import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

