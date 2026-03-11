# geosurvey/app/services/plot_service.py

from sqlalchemy.orm import Session
from app.models import OceanData
import matplotlib.pyplot as plt
from io import BytesIO
import math


def generate_temperature_plot(db: Session, depth: float, anomalies: list):
    records = (
        db.query(OceanData)
        .filter(OceanData.depth == depth)
        .order_by(OceanData.recorded_at)
        .all()
    )

    if not records:
        return None

    times = [r.recorded_at for r in records]
    temps = [r.temperature for r in records]

    mean = sum(temps) / len(temps)
    variance = sum((t - mean) ** 2 for t in temps) / len(temps)
    std_dev = math.sqrt(variance)

    anomaly_ids = {a["id"] for a in anomalies}
    anomaly_times = [r.recorded_at for r in records if r.id in anomaly_ids]
    anomaly_temps = [r.temperature for r in records if r.id in anomaly_ids]

    plt.figure(figsize=(12, 6))
    plt.plot(times, temps)
    plt.scatter(anomaly_times, anomaly_temps)

    plt.axhline(mean)
    plt.axhline(mean + 3 * std_dev)
    plt.axhline(mean - 3 * std_dev)

    plt.title(f"Temperature vs Time at Depth {depth} m")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    return buffer