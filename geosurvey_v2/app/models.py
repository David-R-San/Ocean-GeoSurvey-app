from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class OceanData(Base):
    __tablename__ = "ocean_data"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, index=True)  # deve ser unico pra impedir dublicação 
    site = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    depth = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
