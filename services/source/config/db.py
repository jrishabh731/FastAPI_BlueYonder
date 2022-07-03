from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://postgres:root@10.61.21.144:5432/test_db")
Base = declarative_base()


def get_db_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# engine = create_engine("postgresql://postgres:root@10.61.21.144:5432/test_db")
