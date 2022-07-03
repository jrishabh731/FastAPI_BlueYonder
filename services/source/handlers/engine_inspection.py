import csv
import datetime
from io import StringIO

from source.models.EngineInspectionSchema import EngineInspectionData
from source.schema.EnginePydantic import EngineInspectionSchema
from sqlalchemy.orm import Session
from source.config.db import engine


def get_engine_inspection(id):
    try:
        record = []
        with Session(bind=engine, expire_on_commit=False) as session:
            record = session.query(EngineInspectionData).get(id)
            if record is None:
                record = []
    except Exception as err:
        print(f"Error occured: {err}")
    return {"record": record}


def post_engine_inspection(filedata):
    response = {
        "duplicate_records": [],
        "schema_validations": [],
        "metadata": {
            "inserted_records": 0
        }
    }
    try:
        results = csv.DictReader(StringIO(str(filedata, 'utf-8-sig')), delimiter=',')

        appointment_obj = {}
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
                error_resp = {
                    "error": str(err),
                    "appointmentId": res["appointmentId"],
                    "message": "Schema creation failed for this appointmentID."
                }
                response["schema_validations"].append(error_resp)
            else:
                if obj.appointmentId in appointment_obj:
                    print(f'{obj.appointmentId} is duplicate in the current file, ignoring it.')
                    error_resp = {
                        "message": f'{obj.appointmentId} is duplicate in the file',
                        "appointmentId": res["appointmentId"],
                    }
                    response["duplicate_records"].append(error_resp)
                    continue
                appointment_obj[obj.appointmentId] = EngineInspectionData(**res)

        with Session(bind=engine, expire_on_commit=False) as session:
            records = session.query(EngineInspectionData) \
                .with_entities(EngineInspectionData.appointmentId) \
                .filter(EngineInspectionData.appointmentId.in_(list(appointment_obj.keys())))

        for record in records:
            try:
                if appointment_obj.pop(record.appointmentId, None):
                    error_resp = {
                        "message": f'{record.appointmentId} is already present in DB.',
                        "appointmentId": record.appointmentId
                    }
                    response["duplicate_records"].append(error_resp)
            except Exception as err:
                print(f"Exception: {err}")
        if appointment_obj:
            with Session(bind=engine, expire_on_commit=False) as session:
                session.add_all(appointment_obj.values())
                try:
                    session.commit()
                    response["metadata"]["inserted_records"] = len(appointment_obj)
                except Exception as err:
                    print(err)
        else:
            print("No records left to insert.")
    except Exception as err:
        print(f"Error occured: {err}")
    return response
