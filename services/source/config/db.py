import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
database = os.getenv("POSTGRES_DB")
port = os.getenv("DB_PORT")
db_host = os.getenv("DB_HOST")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{port}/{database}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# engine = create_engine("postgresql://postgres:root@10.61.21.144:5432/test_db")
