
import os
import json
from openai import OpenAI


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_API_TOKEN"],
)


def serialize_events(events):

    serialized = []

    for e in events:
        serialized.append({
            "depth": e["depth"],
            "start": str(e["start"]),
            "end": str(e["end"]),
            "duration_minutes": e["duration_minutes"],
            "max_temperature": e["max_temperature"],
            "points": e["points"]
        })

    return serialized


def generate_llm_report(global_metrics, by_depth, by_site, events):

    structured_data = {
        "dataset_summary": global_metrics,
        "depth_profiles": by_depth,
        "site_profiles": by_site,
        "thermal_events": serialize_events(events)
    }

    prompt = f"""
    
You are an oceanographic data analyst preparing a technical monitoring report.

DATA:
{json.dumps(structured_data, indent=2)}

Generate a clear and objective technical report based strictly on the provided data.

The report must be written for environmental monitoring and operational decision support.

Structure the report with the following sections:

1. Executive Summary
Provide a concise overview of the dataset, the main temperature patterns observed, and whether any thermal anomalies were detected.

2. Dataset Overview
Describe the dataset size, monitoring locations, depth ranges, and general characteristics of the measurements.

3. Temperature Analysis
Summarize the main temperature patterns including:
- average temperature
- temperature variation by depth
- differences between monitoring sites
- evidence of thermal stratification

4. Detected Thermal Events
Describe any detected anomalous thermal events including:
- depth
- start time
- end time
- duration
- maximum temperature
- anomaly intensity relative to historical mean

If no events are detected, clearly state that no significant anomalies were identified.

5. Operational Interpretation
Provide a technical interpretation of the observations focusing on:
- stability of the thermal profile
- presence or absence of abnormal thermal behavior
- monitoring implications

Important rules:
- Base all statements strictly on the provided data.
- Do not speculate about geological or environmental causes unless supported by the data.
- If the cause of an anomaly cannot be determined, explicitly state that further investigation is required.
- Maintain a precise, neutral, and technical tone suitable for environmental monitoring reports.

"""

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=800
    )

    return completion.choices[0].message.content