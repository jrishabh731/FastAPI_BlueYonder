FROM python:3.9
WORKDIR /by
COPY . /by/
RUN pip install --no-cache-dir --upgrade -r /by/requirements.txt
#COPY ./app /code/app

#CMD ["sleep", "1000000"]
CMD ["uvicorn", "source.main:app", "--host", "0.0.0.0", "--port", "80"]
