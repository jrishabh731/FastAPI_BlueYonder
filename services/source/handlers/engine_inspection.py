from source.models.EngineInspectionSchema import EngineInspectionData
from source.schema.EnginePydantic import EngineInspectionSchema
from sqlalchemy.orm import Session
from source.config.db import engine
from fastapi import status, HTTPException


class EngineInspection:
    def __init__(self, session=None):
        self.session = session or Session

    def get_engine_inspection(self, id):
        record = []
        try:
            with self.session(bind=engine, expire_on_commit=False) as session:
                record = session.query(EngineInspectionData).get(id)
                if record is None:
                    record = []
        except Exception as err:
            print(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err
        return {"record": record}

    @staticmethod
    def get_all_records_with_filter(self, table, filter_stmt):
        try:
            with Session(bind=engine, expire_on_commit=False) as session:
                return session.query(table) \
                    .with_entities(EngineInspectionData.appointmentId) \
                    .filter(filter_stmt)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err

    def post_engine_inspection(self, filedata):
        response = {
            "duplicate_records": [],
            "schema_validations": [],
            "metadata": {
                "inserted_records": 0
            }
        }
        try:
            # results = csv.DictReader(StringIO(str(filedata, 'utf-8-sig')), delimiter=',')
            appointment_obj = {}
            cnt = 0
            for result in filedata:
                if cnt == 10000:
                    break
                cnt += 1
                res = dict(result)
                res["inspectionDate"] = res.pop("inspection date", None)
                res["inspectionStartTime"] = res.pop("inspection time", "")
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

            records = self.get_all_records_with_filter(EngineInspectionData,
                                                  EngineInspectionData.appointmentId.in_(list(appointment_obj.keys())))

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
                with self.session(bind=engine, expire_on_commit=False) as session:
                    session.add_all(appointment_obj.values())
                    try:
                        session.commit()
                        response["metadata"]["inserted_records"] = len(appointment_obj)
                    except Exception as err:
                        print(err)
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Exception occured : {err}",
                        ) from err

        except Exception as err:
            print(f"Error occured: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exception occured : {err}",
            ) from err
        return response
