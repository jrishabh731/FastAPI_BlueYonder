from pydantic import BaseModel


class EngineInspection(BaseModel):
    id: int
    label: str

    class Config:
        orm_mode = True