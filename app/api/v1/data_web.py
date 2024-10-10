from app.services.sensor_data_batch import get_sensor_data
from fastapi import APIRouter, Depends
from app.models.device_states import DeviceState
from app.models.devices import Device
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_async_db
from typing import Optional
from fastapi import Query
from sqlalchemy import select, func

router = APIRouter()


@router.get("/")
async def get_sensor_data_batch(
    sensor_id: Optional[int] = None,  # Parámetro opcional para filtrar por sensor
    limit: int = Query(10, ge=1, le=100),  # Número máximo de registros por página (entre 1 y 100)
    offset: int = Query(0, ge=0),  # Desplazamiento para la paginación
    db: AsyncSession = Depends(get_async_db)
):
    return await get_sensor_data(db, sensor_id, limit, offset)

@router.get("/devices")
async def get_sensor_data_batch(
    db: AsyncSession = Depends(get_async_db)
):
    # Subconsulta para obtener el último timestamp de cada device_id
    subquery = (
        select(DeviceState.device_id, func.max(DeviceState.created_at).label("latest_timestamp"))
        .group_by(DeviceState.device_id)
        .subquery()
    )

    # Consulta principal para obtener el estado más reciente
    query = (
        select(DeviceState, Device.name)
        .join(subquery,
              (DeviceState.device_id == subquery.c.device_id) & (DeviceState.created_at == subquery.c.latest_timestamp))
        .join(Device, DeviceState.device_id == Device.id)
    )
    print(query)
    result = await db.execute(query)
    device_states = result.fetchall()
    for x in device_states:
        print(str(x))
    # Estructurar la respuesta en una lista de diccionarios
    return [
        {
            "device_id": ds[0].device_id,
            "name": ds[1],  # Añadimos el nombre del dispositivo
            "state": ds[0].state,
            "timestamp": ds[0].created_at
        } for ds in device_states
    ]
