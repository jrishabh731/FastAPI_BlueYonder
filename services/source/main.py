from fastapi import FastAPI, File, UploadFile
from sqlalchemy.orm import Session

import csv
from source.models.EngineData import EngineInspection

import models.EngineData


app = FastAPI()


@app.get("/get_record/{appointment_id}")
def create_file(appointment_id):
    return {"ID": appointment_id}


@app.post("/upload_data/")
async def create_upload_file(file: UploadFile = File(...)):
    data = await file.read()

    str_data = str(data, 'utf-8')
    print(str_data)
    results = csv.DictReader(str_data)
    # results = [row for row in results]
    # print(results[0])

    return {"filename": file.filename, "data": len(data)}


@app.post("/insert/")
def write_sample(sample: EngineInspection):
    db = Session()
    print(db)
    row = models.EngineData.EngineInspection(sample.id, sample.label)
    return {"status": True}

