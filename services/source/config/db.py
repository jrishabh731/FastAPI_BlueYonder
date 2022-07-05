import os
import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
database = os.getenv("POSTGRES_DB")
port = os.getenv("DB_PORT")
db_host = os.getenv("DB_HOST")
log = logging.getLogger("API_LOG")


def initialize_engine():
    while True:
        try:
            engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{port}/{database}")
            session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return engine, session_local
        except Exception as err:
            log.error(f"Exception occured while connecting to db: {err}")
        time.sleep(10)


engine, SessionLocal = initialize_engine()

Base = declarative_base()

# engine = create_engine("postgresql://postgres:root@10.61.21.144:5432/test_db")
