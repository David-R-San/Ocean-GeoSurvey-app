
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.database import Base, engine, SessionLocal
from app.models import OceanData
from app.services.metrics_engine import (
    calculate_global_metrics,
    temperature_by_depth,
    temperature_by_site,
)
#from app.services.report_service import generate_report
from fastapi.responses import StreamingResponse
from app.services.plot_service import generate_temperature_plot
from app.services.anomaly_engine import detect_zscore_anomalies, detect_thermal_events

from app.services.report_service import generate_llm_report

from fastapi.responses import FileResponse
from app.services.pdf_service import generate_pdf

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ocean GeoSurvey")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file, encoding="latin1")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    required_columns = [
        "ID", "Site", "Latitude", "Longitude",
        "Date", "Time", "Temp (°C)", "Depth"
    ]

    if not all(col in df.columns for col in required_columns):
        raise HTTPException(status_code=400, detail="Invalid dataset structure")

    # Combine date + time robustly
    df["recorded_at"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        errors="coerce"
    )

    # Convert numeric columns safely
    df["Temp (°C)"] = pd.to_numeric(df["Temp (°C)"], errors="coerce")
    df["Depth"] = pd.to_numeric(df["Depth"], errors="coerce")
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    # Remove invalid rows
    df = df.dropna(subset=[
        "Temp (°C)",
        "Depth",
        "Latitude",
        "Longitude",
        "recorded_at"
    ])

    if df.empty:
        raise HTTPException(status_code=400, detail="No valid rows after cleaning")

    try:
        objects = [
            OceanData(
                external_id=int(row.ID),
                site=row.Site,
                latitude=float(row.Latitude),
                longitude=float(row.Longitude),
                temperature=float(row._7),  # Temp (°C)
                depth=float(row.Depth),
                recorded_at=row.recorded_at
            )
            for row in df.itertuples()
        ]

        db.bulk_save_objects(objects)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Dataset uploaded successfully",
        "rows_inserted": len(objects)
    }

@app.delete("/data")
def delete_all_data(db: Session = Depends(get_db)):
    deleted = db.query(OceanData).delete()
    db.commit()

    return {
        "message": "All ocean data deleted",
        "rows_deleted": deleted
    }


@app.get("/metrics/")
def get_metrics(db: Session = Depends(get_db)):
    global_metrics = calculate_global_metrics(db)
    by_depth = temperature_by_depth(db)
    by_site = temperature_by_site(db)

    return {
        "global": global_metrics,
        "by_depth": by_depth,
        "by_site": by_site,
    }

@app.get("/anomalies/")
def get_anomalies(threshold: float = 3.0, db: Session = Depends(get_db)):
    anomalies = detect_zscore_anomalies(db, threshold)
    return {
        "threshold": threshold,
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    }
@app.get("/plot/")
def plot_temperature(depth: float, threshold: float = 3.0, db: Session = Depends(get_db)):
    anomalies = detect_zscore_anomalies(db, threshold)
    filtered_anomalies = [a for a in anomalies if a["depth"] == depth]

    image = generate_temperature_plot(db, depth, filtered_anomalies)

    if image is None:
        raise HTTPException(status_code=404, detail="No data for this depth")

    return StreamingResponse(image, media_type="image/png")

@app.get("/events/")
def get_events(threshold: float = 3.0, db: Session = Depends(get_db)):
    anomalies = detect_zscore_anomalies(db, threshold)
    events = detect_thermal_events(anomalies)

    return {
        "total_events": len(events),
        "events": events
    }


@app.get("/llm-report/")
def llm_report(db: Session = Depends(get_db)):

    global_metrics = calculate_global_metrics(db)
    by_depth = temperature_by_depth(db)
    by_site = temperature_by_site(db)

    anomalies = detect_zscore_anomalies(db)
    events = detect_thermal_events(anomalies)

    report = generate_llm_report(
        global_metrics,
        by_depth,
        by_site,
        events
    )

    return {"llm_report": report}

'''
@app.get("/llm-report-pdf")
def llm_report_pdf(db: Session = Depends(get_db)):

    global_metrics = calculate_global_metrics(db)
    by_depth = temperature_by_depth(db)
    by_site = temperature_by_site(db)

    events = detect_thermal_events(db)

    report = generate_llm_report(
        global_metrics,
        by_depth,
        by_site,
        events
    )

    pdf_path = generate_pdf(report)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="ocean_anomaly_report.pdf"
    )

    '''