import csv
import datetime
from io import StringIO

from fastapi import FastAPI, status, UploadFile, File
from source.config.db import Base, engine
from source.models.EngineInspectionSchema import EngineInspectionData
from sqlalchemy.orm import Session
from source.schema.EnginePydantic import EngineInspectionSchema
from source.handlers.engine_inspection import get_engine_inspection

Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


@app.get("/get_record", status_code=200)
def get_inspection_details(id: str):
    id = f"aj_{id}"
    import pdb
    # pdb.set_trace()
    with Session(bind=engine, expire_on_commit=False) as session:
        record = session.query(EngineInspectionData).get(id)
        if record is None:
            record = []

    return {"record": record}


@app.post("/upload_file/", status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile=File(default=None, media_type="multipart/form-data")):
    data = await file.read()
    str_data = StringIO(str(data, 'utf-8-sig'))
    results = csv.DictReader(str_data, delimiter=',')
    response = {
        "duplicate_records": [],
        "schema_validations": [],
        "metadata": {
            "inserted_records": 0
        }
    }

    appointment_ids = []
    appointment_obj = []
    cnt = 0
    for result in results:
        if cnt == 10000:
            break
        cnt += 1
        res = dict(result)
        res["inspectionDate"] = res.pop("inspection date", None)
        dt_inspectionDate = datetime.datetime.strptime(res["inspectionDate"], "%d-%m-%Y")
        res["inspectionDate"] = dt_inspectionDate.strftime("%m-%d-%Y")
        res["inspectionStartTime"] = res.pop("inspection time", "").split(" ")[-1]
        try:
            obj = EngineInspectionSchema(**res)

        except Exception as err:
            print(f"Error found : {err}")
            print(res)
            error_resp = {
                "error": str(err),
                "appointmentId": res["appointmentId"],
                "message": "Schema creation failed for this appointmentID."
            }
            response["schema_validations"].append(error_resp)
        else:
            if obj.appointmentId in appointment_ids:
                print(f'{obj.appointmentId} is duplicate in the current file, ignoring it.')
                error_resp = {
                    "message": f'{obj.appointmentId} is duplicate in the file',
                    "appointmentId": res["appointmentId"],
                }
                response["duplicate_records"].append(error_resp)
                continue
            appointment_ids.append(obj.appointmentId)
            appointment_obj.append(EngineInspectionData(**res))


    with Session(bind=engine, expire_on_commit=False) as session:
        records = session.query(EngineInspectionData)\
            .with_entities(EngineInspectionData.appointmentId)\
            .filter(EngineInspectionData.appointmentId.in_(appointment_ids))
    for record in records:
        try:
            indx = appointment_ids.index(record.appointmentId)
            appointment_ids.pop(indx)
            appointment_obj.pop(indx)
            error_resp = {
                "message": f'{record.appointmentId} is already present in DB.',
                "appointmentId": record.appointmentId
            }
            response["duplicate_records"].append(error_resp)
        except Exception as err:
            print(f"Exception: {err}")
    if appointment_obj:
        with Session(bind=engine, expire_on_commit=False) as session:
            session.add_all(appointment_obj)
            try:
                session.commit()
                response["metadata"]["inserted_records"] = len(appointment_obj)
            except Exception as err:
                pass
    else:
        print("No records left to insert.")

    return response
