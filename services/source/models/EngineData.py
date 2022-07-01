from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import MetaData

from source.config.db import Base

class EngineInspection(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(256), nullable=False)

