from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List, Optional
# Change from: from Day4.refactor.repository import *
from .repository import *
from .services import *
from .models import *
from .database import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Diabetes Readmission Intervention Queue", version="1.0")

@app.get("/api/queue", response_model=List[PatientEncounter])
def get_queue(limit: int = 50):
    try:
        return fetch_patient_queue(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interventions", response_model=CareInterventionResponse)
def create_new_intervention(payload: CareInterventionCreate):
    try:
        result = add_intervention(payload.encounter_id, payload.assigned_to, payload.notes)
        if not result:
            raise HTTPException(status_code=404, detail="Encounter not found or failed to create intervention")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class InterventionUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

@app.get("/api/queue", response_model=List[PatientEncounter])
def get_queue(limit: int = 50):
    try:
        return fetch_patient_queue(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interventions", response_model=CareInterventionResponse)
def create_new_intervention(payload: CareInterventionCreate):
    try:
        result = add_intervention(payload.encounter_id, payload.assigned_to, payload.notes)
        if not result:
            raise HTTPException(status_code=404, detail="Encounter not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/interventions", response_model=List[CareInterventionResponse])
def get_interventions():
    try:
        return list_interventions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/interventions/{intervention_id}", response_model=CareInterventionResponse)
def update_intervention(intervention_id: int, payload: InterventionUpdate):
    try:
        result = modify_intervention_status(intervention_id, payload.status, payload.notes)
        if not result:
            raise HTTPException(status_code=404, detail="Intervention ID not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/queue/high-risk", response_model=List[PatientEncounter])
def get_high_risk_queue_endpoint(limit: int = 50):
    try:
        return fetch_high_risk_queue(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/queue/{encounter_id}")
def get_encounter(encounter_id: int):
    res = get_encounter_by_id(encounter_id)
    if not res:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return res

@app.get("/api/interventions/{intervention_id}")
def get_intervention(intervention_id: int):
    res = get_intervention_by_id(intervention_id)
    if not res:
        raise HTTPException(status_code=404, detail="Intervention not found")
    return res

@app.get("/api/stats")
def get_stats():
    return get_queue_stats()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)