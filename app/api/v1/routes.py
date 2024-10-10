# app/api/v1/routes.py
from fastapi import APIRouter
from app.api.v1.data import router as data_in_router
from app.api.v1.data_web import router as data_web_router
router = APIRouter()

router.include_router(data_in_router, prefix="/data_in", tags=["data_node"])
router.include_router(data_web_router, prefix="/web_apis", tags=["web-data"])