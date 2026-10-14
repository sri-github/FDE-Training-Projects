# Diabetes Readmission & Clinical Intervention Queue (Day 4 FDE) 
A robust backend architecture and data pipeline built for healthcare operational analytics, featuring PostgreSQL ingestion, raw SQL repository patterns, Pydantic data validation, and FastAPI service routing. --- 
## Architecture Overview 
[ FastAPI Endpoint (main.py) ] │ 
▼ [ Business Logic / Services (services.py) ] │ 
▼ [ Data Access / Repository (repository.py) ] │ 
▼ [ Database Connection Pool (database.py) ] ──> [ PostgreSQL (`diabetes_queue_db`) ] 

### 1. Persistence Hook (`database.py`)

* **Role**: Manages database connectivity using `psycopg`.
* **Data Handling**: Configures connection strings with secure classroom credentials (`fde_user`) and utilizes `dict_row` row factories so that raw SQL query results map directly into structured Python dictionaries.

### 2. Pydantic Models Layer (`models.py`)

* **Role**: Data validation and type safety.
* **Data Handling**: Defines request and response schemas (e.g., `PatientEncounter`, `CareInterventionCreate`, `CareInterventionResponse`) to validate incoming payloads and serialize database records into strict JSON responses for API consumers.

### 3. Data Access / Repository Layer (`repository.py`)

* **Role**: Database operations and raw SQL execution.
* **Data Handling**: Isolates all database queries away from business logic. It handles `SELECT` queries for fetching patient queues, `INSERT` statements for logging new care interventions, and `UPDATE` statements for modifying clinical intervention statuses.

### 4. Business Logic / Services Layer (`services.py`)

* **Role**: Domain rules and workflow orchestration.
* **Data Handling**: Acts as an intermediary between FastAPI endpoints and the repository layer. It processes high-risk filtering rules, coordinates intervention assignments, and manages operational state transitions.

### 5. API Routing Layer (`main.py`)

* **Role**: HTTP interface and endpoint exposure.
* **Data Handling**: Exposes REST endpoints via FastAPI, translates incoming HTTP requests into service calls, handles error exceptions, and powers the interactive OpenAPI Swagger documentation (`/docs`).

---

## Database Schema & Data Flow

The database (`diabetes_queue_db`) consists of two relational tables:

1. **`patient_encounters`**: Stores immutable historical patient data, length of hospital stays, lab counts, and readmission indicators.
2. **`care_interventions`**: A one-to-many operational table referencing `patient_encounters(encounter_id)` via a foreign key constraint. It logs clinical actions, reviewer assignments, and review statuses (`PENDING_REVIEW`, `IN_PROGRESS`, `COMPLETED`).

---

## API Endpoints Reference

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/api/queue` | Fetches the standard patient encounter queue. |
| **GET** | `/api/queue/high-risk` | Filters and returns high-priority patient encounters based on readmission risk metrics. |
| **GET** | `/api/interventions` | Lists all logged clinical intervention records. |
| **POST** | `/api/interventions` | Creates a new care intervention linked to a valid patient encounter ID. |
| **PATCH** | `/api/interventions/{id}` | Updates the operational status and clinical notes of an existing intervention, committing changes directly to PostgreSQL. |

---

## Getting Started & Running the App

1. **Start PostgreSQL & Verify Connection**:
Ensure your database is active and `fde_user` has proper permissions on `diabetes_queue_db`.
2. **Run the Data Ingestion Script**:
```powershell
.\.venv\Scripts\python.exe ./Day4/refactor/load_data.py

```


3. **Start the FastAPI Backend**:
```powershell
python -m uvicorn main:app --reload --port 8000

```


4. **Access Swagger UI**:
Navigate to `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)` to test the endpoints interactively.
