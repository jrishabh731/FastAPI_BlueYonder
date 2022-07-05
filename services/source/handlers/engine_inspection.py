from models.EngineInspectionSchema import EngineInspectionData
from schema.EnginePydantic import EngineInspectionSchema
from sqlalchemy.orm import Session
from config.db import engine
from fastapi import status, HTTPException


class EngineInspection:
    def __init__(self, session=None):
        self.session = session or Session

    def get_engine_inspection(self, id):
        """

        :param id:
        :return:
        """
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
    def get_all_records_with_filter(table, filter_stmt):
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

    @staticmethod
    def validate_schema_and_deduplicate(record, filtered_records, error_response):
        """
        Validate Schema for the given record. If schema is valid then the record
        shouldn't be already present in the current filtered records.
        Adds error response to passed dictionary.
        Adds filtered and valid record to shared filtered_records object
        :param record: dict,
        :param error_response: dict,
        :param filtered_records: Updates filtered records with a new key and value
                                 key: appointmentID and value the converted schema
        """
        # As these columns have
        record["inspectionDate"] = record.pop("inspection date", None)
        record["inspectionStartTime"] = record.pop("inspection time", "")
        try:
            obj = EngineInspectionSchema(**record)
        except Exception as err:
            error_resp = {
                "error": str(err),
                "appointmentId": record["appointmentId"],
                "message": "Schema creation failed for this appointmentID."
            }
            error_response["schema_validations"].append(error_resp)
        else:
            if obj.appointmentId in filtered_records:
                print(f'{obj.appointmentId} is duplicate in the current file, ignoring it.')
                error_resp = {
                    "message": f'{obj.appointmentId} is duplicate in the file',
                    "appointmentId": record["appointmentId"],
                }
                error_response["duplicate_records"].append(error_resp)
                return
            filtered_records.update({obj.appointmentId: EngineInspectionData(**record)})

    def drop_already_existing_records(self, filtered_records, error_response):
        """

        :param filtered_records:
        :param error_response:
        :return:
        """
        # Calls function to get records which match the give filter
        records = self.get_all_records_with_filter(
            EngineInspectionData, EngineInspectionData.appointmentId.in_(list(filtered_records.keys()))
        )

        for record in records:
            try:
                if filtered_records.pop(record.appointmentId, None):
                    error_resp = {
                        "message": f'{record.appointmentId} is already present in DB.',
                        "appointmentId": record.appointmentId
                    }
                    error_response["duplicate_records"].append(error_resp)
            except Exception as err:
                print(f"Exception: {err}")

    def post_engine_inspection(self, filedata):
        """
        This functions creates pydantic schema objects for each record and filters
        non-unique records. Records with already existing primary key are also filtered.
        Remaining records are inserted to DB.
        :param filedata: List[dict]
        :return:
        {
            "duplicate_records": [], # Duplicate records in the input file.
            "schema_validations": [], # Records which have schema issues.
            "metadata": {
                "inserted_records": 0 # No of records inserted to database.
            }
        }
        """
        error_response = {
            "duplicate_records": [],
            "schema_validations": [],
            "metadata": {
                "inserted_records": 0
            }
        }
        try:
            filtered_records = {}
            for result in filedata:
                self.validate_schema_and_deduplicate(dict(result), filtered_records, error_response)

            self.drop_already_existing_records(filtered_records, error_response)

            if filtered_records:
                with self.session(bind=engine, expire_on_commit=False) as session:
                    session.add_all(filtered_records.values())
                    try:
                        session.commit()
                        error_response["metadata"]["inserted_records"] = len(filtered_records)
                    except Exception as err:
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
        return error_response
