# Ocean-GeoSurvey-app

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green)
![Data Analysis](https://img.shields.io/badge/Data%20Analysis-pandas-yellow)
![AI Report](https://img.shields.io/badge/AI-LLM%20report-purple)
![Status](https://img.shields.io/badge/status-prototype-orange)

Prototype system for processing oceanographic temperature data, detecting thermal anomalies, and generating automated technical monitoring reports.

The system ingests ocean sensor datasets, performs statistical analysis, detects anomalous temperature behavior, groups anomalies into thermal events, and generates AI-assisted reports.

---

# API Overview

Example of the API endpoints available through the FastAPI interactive documentation.

<img width="1834" height="715" alt="image" src="https://github.com/user-attachments/assets/a514c88b-7caa-4326-87e4-db481fda2338" />


The endpoints can be tested directly through the FastAPI documentation interface available at:
http://127.0.0.1:8000/docs


---

# Features

- Upload ocean sensor datasets (CSV)
- Store measurements in a database
- Compute global dataset metrics
- Detect anomalous temperature measurements using statistical methods
- Identify thermal events from grouped anomalies
- Generate AI-assisted technical monitoring reports
- Reset the dataset when needed

---

# Installation

Clone the repository:
```bash
git clone https://github.com/your-repo/ocean-geosurvey.git
cd ocean-geosurvey
```
Create a Conda environment:
```bash
conda create -n geo python=3.11
conda activate geo
```
Install project dependencies:
```bash
pip install -r requirements.txt
```

Running the API

Start the server:
```bash
uvicorn app.main:app --reload
```

##Usage Workflow
1 Upload dataset
POST /upload

2 Retrieve dataset metrics
GET /metrics

3 Detect anomalous temperature measurements
GET /anomalies

4 Detect thermal events
GET /events

5 Generate AI technical report
GET /llm-report

6 Reset dataset(optional)
DELETE /data


##Notes

This project is a prototype intended to demonstrate:

-backend API development

-environmental data processing

-anomaly detection

-AI-assisted reporting

-Some components (such as advanced error handling and full production hardening) are still under development.

Author:

David R.de Santana


