from fastapi import HTTPException
from sqlalchemy.future import select
from app.models.sensors import Sensor
from app.models.sensor_data import SensorData


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