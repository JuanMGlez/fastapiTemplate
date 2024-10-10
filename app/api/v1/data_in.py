from app.services.sensor_data_batch import data_in_service
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_async_db
from typing import Dict, Any

router = APIRouter()

@router.post("/")
async def create_sensor_data_batch(sensor_data_batch: Dict[str, Any], db: AsyncSession = Depends(get_async_db)):
    return await data_in_service(db, sensor_data_batch)

