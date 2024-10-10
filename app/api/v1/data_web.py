from app.services.sensor_data_batch import get_sensor_data
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_async_db
from typing import Optional
from fastapi import Query

router = APIRouter()


@router.get("/")
async def get_sensor_data_batch(
    sensor_id: Optional[int] = None,  # Parámetro opcional para filtrar por sensor
    limit: int = Query(10, ge=1, le=100),  # Número máximo de registros por página (entre 1 y 100)
    offset: int = Query(0, ge=0),  # Desplazamiento para la paginación
    db: AsyncSession = Depends(get_async_db)
):
    return await get_sensor_data(db, sensor_id, limit, offset)

