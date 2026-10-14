from pydantic import BaseModel
from typing import Optional, List

class PatientEncounter(BaseModel):
    encounter_id: int
    patient_nbr: int
    age: Optional[str] = None
    time_in_hospital: Optional[int] = None
    number_inpatient: Optional[int] = None
    number_emergency: Optional[int] = None
    number_outpatient: Optional[int] = None
    num_medications: Optional[int] = None
    num_lab_procedures: Optional[int] = None
    readmitted: Optional[str] = None
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None

    class Config:
        from_attributes = True

class CareInterventionCreate(BaseModel):
    encounter_id: int
    assigned_to: str
    notes: Optional[str] = None

class CareInterventionResponse(BaseModel):
    intervention_id: int
    encounter_id: int
    status: str
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True