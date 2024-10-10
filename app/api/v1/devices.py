from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.postgres import get_async_db  # Asegúrate de que este se refiere a la sesión asíncrona
from app.models.device_states import DeviceState
from app.schemas.devices import DeviceStateResponse, DeviceStateCreate
from app.schemas.ws import ConnectionManager
from app.services.sensor_data_batch import web_sock

manager = ConnectionManager()

router = APIRouter()

# Endpoint para crear un nuevo dispositivo y su estado (inserción)
@router.post("/", response_model=DeviceStateResponse, status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceStateCreate, db: AsyncSession = Depends(get_async_db)):
    new_device = DeviceState(
        device_id=device.device_id,
        state=device.state,
        description=device.description
    )
    db.add(new_device)
    await db.commit()
    await db.refresh(new_device)

    # Enviar notificación a través de WebSocket
    await manager.send_message({"id": new_device.id, "device_id": new_device.device_id, "state": new_device.state})

    return new_device

# WebSocket endpoint
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await web_sock(websocket)


