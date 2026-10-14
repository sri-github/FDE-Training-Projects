import os
import pandas as pd
import psycopg
from database import DATABASE_URL

# Resolve absolute path to diabetic_data.csv inside the Day4/data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "data", "diabetic_data.csv")

# Load the official dataset CSV
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} rows from CSV. Inserting into PostgreSQL...")

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO patient_encounters (
                    encounter_id, patient_nbr, age, time_in_hospital, 
                    number_inpatient, number_emergency, number_outpatient, 
                    num_medications, num_lab_procedures, discharge_disposition_id, 
                    admission_type_id, readmitted, risk_score, risk_level
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (encounter_id) DO NOTHING;
                """,
                (
                    row.get("encounter_id"),
                    row.get("patient_nbr"),
                    str(row.get("age", "")),
                    int(row.get("time_in_hospital", 0)),
                    int(row.get("number_inpatient", 0)),
                    int(row.get("number_emergency", 0)),
                    int(row.get("number_outpatient", 0)),
                    int(row.get("num_medications", 0)),
                    int(row.get("num_lab_procedures", 0)),
                    int(row.get("discharge_disposition_id", 0)),
                    int(row.get("admission_type_id", 0)),
                    str(row.get("readmitted", "NO")),
                    50,
                    "MEDIUM"
                )
            )
    conn.commit()
print("Data loading complete!")