

from fastapi import FastAPI, status, UploadFile, File
from source.config.db import Base, engine
from source.models.EngineInspectionSchema import EngineInspectionData
from sqlalchemy.orm import Session
from source.schema.EnginePydantic import EngineInspectionSchema
from source.handlers.engine_inspection import get_engine_inspection, post_engine_inspection

# Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


@app.get("/get_record", response_model=EngineInspectionSchema, status_code=200)
def get_inspection_details(id: str):
    return get_engine_inspection(f"aj_{id}")


@app.post("/upload_file/", status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile=File(default=None, media_type="multipart/form-data")):
    data = await file.read()
    return post_engine_inspection(data)
