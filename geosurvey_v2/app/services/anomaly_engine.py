import matplotlib
matplotlib.use("Agg")
from sqlalchemy.orm import Session
from app.models import OceanData
import math
from datetime import timedelta


def detect_zscore_anomalies(db: Session, threshold: float = 3.0):
    anomalies = []

    depths = db.query(OceanData.depth).distinct().all()

    for (depth,) in depths:
        records = (
            db.query(OceanData)
            .filter(OceanData.depth == depth)
            .order_by(OceanData.recorded_at)
            .all()
        )

        if len(records) < 2:
            continue

        temperatures = [r.temperature for r in records]
        mean = sum(temperatures) / len(temperatures)
        variance = sum((t - mean) ** 2 for t in temperatures) / len(temperatures)
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            continue

        for r in records:
            z_score = (r.temperature - mean) / std_dev
            if abs(z_score) >= threshold:
                anomalies.append({
                    "id": r.id,
                    "depth": r.depth,
                    "temperature": r.temperature,
                    "z_score": round(z_score, 3),
                    "recorded_at": r.recorded_at,
                    "mean": mean,
                    "std_dev": std_dev
                })

    return anomalies


def detect_thermal_events(anomalies: list, max_gap_minutes: int = 40):
    if not anomalies:
        return []

    anomalies_sorted = sorted(anomalies, key=lambda x: x["recorded_at"])
    events = []
    current_event = [anomalies_sorted[0]]

    for prev, curr in zip(anomalies_sorted, anomalies_sorted[1:]):
        gap = curr["recorded_at"] - prev["recorded_at"]

        if gap <= timedelta(minutes=max_gap_minutes):
            current_event.append(curr)
        else:
            events.append(current_event)
            current_event = [curr]

    events.append(current_event)

    summarized = []
    for event in events:
        start = event[0]["recorded_at"]
        end = event[-1]["recorded_at"]
        duration = (end - start).total_seconds() / 60

        max_temperature = max(e["temperature"] for e in event)
        mean = event[0]["mean"]
        intensity = max_temperature - mean

        summarized.append({
            "depth": event[0]["depth"],
            "start": start,
            "end": end,
            "duration_minutes": duration,
            "max_temperature": max_temperature,
            "thermal_intensity": round(intensity, 2),
            "points": len(event)
        })

    return summarized