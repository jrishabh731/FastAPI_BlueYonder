from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import StringIO
import csv

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

