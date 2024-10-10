# app/api/v1/routes.py
from fastapi import APIRouter
from app.api.v1.data import router as data_in_router
from app.api.v1.data_web import router as data_web_router
from app.api.v1.devices import router as device_data
router = APIRouter()

router.include_router(data_in_router, prefix="/data_in", tags=["data_node"])
router.include_router(data_web_router, prefix="/web_apis", tags=["web-data"])
router.include_router(device_data, prefix="/devices_apis", tags=["device-data"])