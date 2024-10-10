from fastapi import HTTPException
from sqlalchemy.future import select
from app.models.sensors import Sensor
from app.models.sensor_data import SensorData
from sqlalchemy.sql import func
from typing import Optional
from fastapi import Query
from app.schemas import sensor_data as schemas
from app.schemas.sensor_data import PaginatedSensorData

async def data_in_service(db, sensor_data_batch):
    data_format = []
    temp_data = {}
    for batch in sensor_data_batch:
        if batch.startswith("sensor_id_"):
            temp_data["id"]= sensor_data_batch[batch]
        else:
            temp_data["value"] = sensor_data_batch[batch]
            data_format.append(temp_data)
            temp_data = {}

    # Validar que todos los sensores existan
    for sensor_key in data_format:
        sensor_id = sensor_key["id"]
        result = await db.execute(select(Sensor).filter(Sensor.id == sensor_id))
        sensor = result.scalars().first()
        if sensor is None:
            raise HTTPException(status_code=404, detail=f"Sensor con id {sensor_id} no encontrado")
    db_sensor_data = SensorData()
    # Insertar los datos de cada sensor en la base de datos
    for sensor_key in data_format:
        sensor_id = sensor_key["id"]
        value = sensor_key["value"]

        db_sensor_data = SensorData(
            sensor_id=sensor_id,
            value=value
        )
        db.add(db_sensor_data)

        # Confirmar los cambios en la base de datos
    await db.commit()
    await db.refresh(db_sensor_data)  # Obtener los datos actualizados
    return db_sensor_data

async def get_sensor_data(
    db,
    sensor_id: Optional[int] = None,  # Parámetro opcional para filtrar por sensor
    limit: int = Query(10, ge=1, le=100),  # Número máximo de registros por página (entre 1 y 100)
    offset: int = Query(0, ge=0),  # Desplazamiento para la paginación
):
    # Consulta para contar el número total de registros
    total_query = select(func.count(SensorData.id))
    print(total_query)
    if sensor_id:  # Si se pasa un sensor_id, filtramos los registros
        total_query = total_query.filter(SensorData.sensor_id == sensor_id)
        print("Hell no", sensor_id)
    total_result = await db.execute(total_query)
    total = total_result.scalar()
    print(total)

    # Consulta para obtener los registros con paginación
    query = select(SensorData).offset(offset).limit(limit).order_by(SensorData.recorded_at.desc())
    if sensor_id:  # Si se pasa un sensor_id, filtramos los registros
        query = query.filter(SensorData.sensor_id == sensor_id)

    result = await db.execute(query)
    sensor_data = result.scalars().all()

    # Estructurar la respuesta paginada
    return PaginatedSensorData(
        total=total,
        data=[schemas.SensorData(
            id=sd.id,
            sensor_id=sd.sensor_id,
            value=sd.value,
            recorded_at=sd.recorded_at
        ) for sd in sensor_data]
    )