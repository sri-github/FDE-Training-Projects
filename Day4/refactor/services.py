from repository import get_high_risk_queue, create_intervention, update_intervention_status, get_all_interventions

def fetch_intervention_queue(limit: int = 50):
    encounters = get_high_risk_queue(limit)
    return encounters

def add_intervention(encounter_id: int, assigned_to: str, notes: str):
    return create_intervention(encounter_id, assigned_to, notes)

def fetch_intervention_queue(limit: int = 50):
    return get_high_risk_queue(limit)

def add_intervention(encounter_id: int, assigned_to: str, notes: str):
    return create_intervention(encounter_id, assigned_to, notes)

def list_interventions():
    return get_all_interventions()

def modify_intervention_status(intervention_id: int, status: str, notes: str = None):
    return update_intervention_status(intervention_id, status, notes)