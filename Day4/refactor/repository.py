from .database import get_connection

# 1. Plain Queue (Unfiltered for /api/queue)
def get_patient_queue(limit: int = 50):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT encounter_id, patient_nbr, age, time_in_hospital, 
                       number_inpatient, number_emergency, number_outpatient, 
                       num_medications, num_lab_procedures, readmitted, risk_score, risk_level
                FROM patient_encounters
                ORDER BY encounter_id DESC
                LIMIT %s;
                """,
                (limit,)
            )
            return cur.fetchall()

def get_high_risk_queue(limit: int = 50):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT encounter_id, patient_nbr, age, time_in_hospital, 
                       number_inpatient, number_emergency, number_outpatient, 
                       num_medications, num_lab_procedures, readmitted, risk_score, risk_level
                FROM patient_encounters
                WHERE risk_score >= 50 OR risk_level IN ('HIGH', 'MEDIUM')
                ORDER BY risk_score DESC
                LIMIT %s;
                """,
                (limit,)
            )
            return cur.fetchall()

def get_queue_stats():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM patient_encounters) AS total_encounters,
                    (SELECT COUNT(*) FROM patient_encounters WHERE risk_score >= 50) AS high_risk_count,
                    (SELECT COUNT(*) FROM care_interventions WHERE status = 'PENDING_REVIEW') AS pending_interventions;
            """)
            return cur.fetchone()

def create_intervention(encounter_id: int, assigned_to: str, notes: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO care_interventions (encounter_id, assigned_to, notes, status)
                VALUES (%s, %s, %s, 'PENDING_REVIEW')
                RETURNING intervention_id, encounter_id, status, assigned_to, notes;
                """,
                (encounter_id, assigned_to, notes)
            )
            conn.commit()
            return cur.fetchone()

def update_intervention_status(intervention_id: int, status: str, notes: str = None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE care_interventions
                SET status = %s, 
                    notes = COALESCE(%s, notes),
                    updated_at = CURRENT_TIMESTAMP
                WHERE intervention_id = %s
                RETURNING intervention_id, encounter_id, status, assigned_to, notes;
                """,
                (status, notes, intervention_id)
            )
            conn.commit()
            return cur.fetchone()

def get_all_interventions():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT intervention_id, encounter_id, status, assigned_to, notes, created_at, updated_at
                FROM care_interventions
                ORDER BY created_at DESC;
                """
            )
            return cur.fetchall()

def get_encounter_by_id(encounter_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM patient_encounters WHERE encounter_id = %s;", (encounter_id,))
            return cur.fetchone()

def get_intervention_by_id(intervention_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM care_interventions WHERE intervention_id = %s;", (intervention_id,))
            return cur.fetchone()
