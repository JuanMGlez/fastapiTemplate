from fastapi import HTTPException
from sqlalchemy.future import select
from app.models.sensors import Sensor
from app.models.sensor_data import SensorData
from sqlalchemy.sql import func
from typing import Optional
from fastapi import Query
from app.schemas import sensor_data as schemas
from app.schemas.sensor_data import PaginatedSensorData
from app.models.device_states import DeviceState
from app.schemas.ws import ConnectionManager
from fastapi import WebSocket

manager = ConnectionManager()


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

    # Ejecutar el algoritmo de optimización aquí
    # Ejecutar el algoritmo de optimización
    temperature_value = next(
        (item['value'] for item in data_format if item['id'] == sensor_data_batch.get("sensor_id_temperature")),
        None  # Valor por defecto si no se encuentra
    )
    motion_value = next(
        (item['value'] for item in data_format if item['id'] == sensor_data_batch.get("sensor_id_motion")),
        None  # Valor por defecto si no se encuentra
    )

    # Obtener el estado de los dispositivos
    device_state_result = await db.execute(select(DeviceState).filter(DeviceState.state == "on"))
    device_states = device_state_result.scalars().all()

    led_states = {
        1: "off",  # Foco
        2: "off",  # Ventilador
        3: "off"  # A/C
    }

    for device_state in device_states:
        led_states[device_state.device_id] = "on"  # Actualizar el estado del LED correspondiente

    await run_optimization(db, {
        "temperature": temperature_value,
        "presence": bool(motion_value),
        "led_states": led_states  # Usar el diccionario de estados de LED con IDs
    })

    #await db.refresh(db_sensor_data)  # Obtener los datos actualizados
    return db_sensor_data


async def run_optimization(db, optimization_data):
    temperature = optimization_data["temperature"]
    presence = optimization_data["presence"]
    led_states = optimization_data["led_states"]

    # Ejemplo de lógica de optimización
    if presence:
        if temperature > 25:  # Si la temperatura es mayor a 25°C
            led_states[1] = "on"  # Encender el foco
            led_states[2] = "on"  # Encender el ventilador
            led_states[3] = "on"  # Apagar el A/C
        elif 20 <= temperature <= 25:  # Temperatura entre 20°C y 25°C
            led_states[1] = "on"  # Apagar el foco
            led_states[2] = "off"  # Mantener el ventilador encendido
            led_states[3] = "on"   # Encender el A/C
        else:  # Si la temperatura es menor a 20°C
            led_states[1] = "on"  # Apagar el foco
            led_states[2] = "off"  # Apagar el ventilador
            led_states[3] = "off"    # Encender el A/C
    else:
        # Si no hay presencia, apaga todos los dispositivos
        led_states[1] = "off"  # Apagar el foco
        led_states[2] = "off"  # Apagar el ventilador
        led_states[3] = "off"   # Apagar el A/C

    # Actualizar el estado de los dispositivos en la base de datos
    for device_id, state in led_states.items():
        if device_id is not None:
            device_state = DeviceState(device_id=device_id, state=state)
            db.add(device_state)
            await manager.send_message({"device_id": device_id, "state": state})

    await db.commit()  # Confirmar cambios en la base de datos

    # Aquí podrías agregar lógica adicional para notificaciones, registros, etc.


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


async def web_sock(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"You wrote: {data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(websocket)