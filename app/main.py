from fastapi import FastAPI
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router as api_router

app = FastAPI()

# Configuración de CORS para permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(api_router, prefix="/api/v1")

# Ruta de salud
@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}