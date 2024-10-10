from app.db.sqlite_conn import get_db

async def data_in_service(db, data):
    for item in data:
        print(item)

    return {"message": "Data received"}