from fastapi import FastAPI, status, UploadFile, File
from config.db import Base, engine
from handlers.engine_inspection import EngineInspection

from utils import Utils
Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/get_record", status_code=200)
def get_inspection_details(id: str):
    return EngineInspection().get_engine_inspection(f"aj_{id}")


@app.post("/upload_file/", status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile = File(default=None, media_type="multipart/form-data")):
    data = await file.read()
    data = Utils.csv_to_dict(data)
    return EngineInspection().post_engine_inspection(data)
