from fastapi import FastAPI, File, UploadFile



app = FastAPI()


@app.get("/get_record/{appointment_id}")
def create_file(appointment_id):
    return {"ID": appointment_id}


@app.post("/upload_data/")
def create_upload_file(file: UploadFile):
    return {"status": 200,
            "filename": file.filename,
            "data": file.read()}
