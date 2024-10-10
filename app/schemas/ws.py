from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

# Administrador de conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


    async def send_message(self, message: dict):
        message_json = json.dumps(message)  # Convierte el mensaje a JSON
        for connection in self.active_connections:
            await connection.send_text(message_json)  # Enviar el JSON como texto
