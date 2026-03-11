from pydantic import BaseModel
from datetime import datetime

class OceanDataBase(BaseModel):
    external_id: int
    site: str
    latitude: float
    longitude: float
    temperature: float
    depth: float
    recorded_at: datetime

class OceanDataResponse(OceanDataBase):
    id: int

    class Config:
        orm_mode = True
