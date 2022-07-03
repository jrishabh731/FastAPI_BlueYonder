from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://postgres:root@10.61.21.144:5432/test_db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# engine = create_engine("postgresql://postgres:root@10.61.21.144:5432/test_db")
