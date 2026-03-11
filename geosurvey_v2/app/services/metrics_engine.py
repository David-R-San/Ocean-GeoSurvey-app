from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import OceanData

def calculate_global_metrics(db: Session):
    total_points = db.query(OceanData).count()
    avg_temp = db.query(func.avg(OceanData.temperature)).scalar()
    avg_depth = db.query(func.avg(OceanData.depth)).scalar()

    return {
        "total_points": total_points,
        "average_temperature": float(avg_temp or 0),
        "average_depth": float(avg_depth or 0),
    }

def temperature_by_depth(db: Session):
    results = (
        db.query(OceanData.depth, func.avg(OceanData.temperature))
        .group_by(OceanData.depth)
        .all()
    )
    return {str(depth): float(temp) for depth, temp in results}

def temperature_by_site(db: Session):
    results = (
        db.query(OceanData.site, func.avg(OceanData.temperature))
        .group_by(OceanData.site)
        .all()
    )
    return {site: float(temp) for site, temp in results}
