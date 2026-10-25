# Diabetes Readmission Intervention Queue & API

A full-stack clinical decision support application built with **FastAPI**, **PostgreSQL**, and a **TypeScript client**, designed to manage hospital patient encounters, calculate dynamic readmission risk scores, and track care interventions.

---

## 🏗️ Architecture & Tech Stack

* **Backend Framework**: Python FastAPI (`main.py`)
* **Data Validation**: Pydantic Models (`models.py`)[cite: 11]
* **Database Layer**: PostgreSQL via `psycopg` with dictionary row factories (`database.py`, `repository.py`)[cite: 8, 12]
* **Business Logic**: Service layer separation (`services.py`)[cite: 13]
* **Data Ingestion**: Automated CSV loader with dynamic risk algorithms (`load_data.py`)
* **Frontend Verification**: TypeScript async `fetch()` client (`homework.ts`) executed via Node.js

---

## 🔌 API Endpoints (8+ Endpoints)

The FastAPI backend exposes the following robust endpoints:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/queue` | `GET` | Retrieve the general patient encounter queue (with limit parameter)[cite: 10, 12]. |
| `/api/queue/high-risk` | `GET` | Retrieve filtered high-risk patient encounters (`risk_score >= 70`)[cite: 10, 12]. |
| `/api/queue/{encounter_id}` | `GET` | Look up an individual patient encounter record by ID[cite: 10, 12]. |
| `/api/interventions` | `GET` | List all clinical care interventions[cite: 10, 12]. |
| `/api/interventions` | `POST` | Create and log a new care intervention (`PENDING_REVIEW`)[cite: 10, 12]. |
| `/api/interventions/{id}` | `GET` | Retrieve a specific intervention record by ID[cite: 10, 12]. |
| `/api/interventions/{id}` | `PATCH` | Update an intervention's status and clinical notes[cite: 10, 12]. |
| `/api/stats` | `GET` | Fetch real-time dashboard metrics (total encounters, high-risk count, pending reviews)[cite: 10, 12]. |

---

## 🧠 Dynamic Risk Calculation Engine

To ensure robust database integration, the data ingestion pipeline (`load_data.py`) processes raw hospital records (`diabetic_data.csv`)[cite: 9] and programmatically computes clinical risk scores based on emergency visits, inpatient admissions, hospital stay duration, and medication counts:
* **HIGH Risk (`>= 70`)**: Prioritized for immediate clinical intervention[cite: 12].
* **MEDIUM / LOW Risk**: Standard monitoring queues.

---

## 🚀 Setup & Execution Guide

### 1. Database & Environment Setup
Ensure your local PostgreSQL service is running and your `.env` file contains your database connection URL (defaulting to `diabetes_queue_db`)[cite: 8]:
```env
DATABASE_URL=postgresql://fde_user:FDE_Local_2026@localhost:5432/diabetes_queue_db