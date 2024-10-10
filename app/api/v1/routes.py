# app/api/v1/routes.py
from fastapi import APIRouter
from app.api.v1.data_in import router as data_in_router
router = APIRouter()

router.include_router(data_in_router, prefix="/data_in", tags=["data_node"])