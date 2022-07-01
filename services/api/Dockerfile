FROM python:3.9
WORKDIR /code
COPY . /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#COPY ./app /code/app

#CMD ["sleep", "1000000"]
CMD ["uvicorn", "source.main:app", "--host", "0.0.0.0", "--port", "80"]
uvicorn source.main:app --host 0.0.0.0 --port 80