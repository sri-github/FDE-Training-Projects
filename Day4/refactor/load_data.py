import os
import pandas as pd
import psycopg
from database import DATABASE_URL
# Resolve absolute path to diabetic_data.csv inside the Day4/data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "diabetic_data.csv")

# Load the official dataset CSV
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} rows from CSV. Clearing existing data and recalculating risk metrics...")

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # Clear existing patient encounters and related interventions to prevent duplicates/stale data
        cur.execute("TRUNCATE TABLE patient_encounters RESTART IDENTITY CASCADE;")
        
        for _, row in df.iterrows():
            # Extract key indicators
            emergencies = int(row.get("number_emergency", 0))
            inpatient = int(row.get("number_inpatient", 0))
            time_hospital = int(row.get("time_in_hospital", 0))
            meds = int(row.get("num_medications", 0))

            # Architectural Risk Scoring Algorithm
            calculated_score = (emergencies * 25) + (inpatient * 20) + (time_hospital * 2) + (meds * 1)
            risk_score = min(calculated_score, 100)

            # Assign categorical risk level
            if risk_score >= 70:
                risk_level = "HIGH"
            elif risk_score >= 40:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

            cur.execute(
                """
                INSERT INTO patient_encounters (
                    encounter_id, patient_nbr, age, time_in_hospital, 
                    number_inpatient, number_emergency, number_outpatient, 
                    num_medications, num_lab_procedures, discharge_disposition_id, 
                    admission_type_id, readmitted, risk_score, risk_level
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    row.get("encounter_id"),
                    row.get("patient_nbr"),
                    str(row.get("age", "")),
                    time_hospital,
                    inpatient,
                    emergencies,
                    int(row.get("number_outpatient", 0)),
                    meds,
                    int(row.get("num_lab_procedures", 0)),
                    int(row.get("discharge_disposition_id", 0)),
                    int(row.get("admission_type_id", 0)),
                    str(row.get("readmitted", "NO")),
                    risk_score,
                    risk_level
                )
            )
    conn.commit()
print("Database cleared, re-seeded, and dynamic risk calculation complete!")