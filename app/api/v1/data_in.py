from fastapi import APIRouter
from app.services.data_in_service import data_in_service
from fastapi import Depends
from app.db.sqlite_conn import get_db
router = APIRouter()

@router.post("/")
async def data_in(data, db=Depends(get_db)):
    return await data_in_service(db, data)

