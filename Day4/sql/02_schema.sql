DROP TABLE IF EXISTS care_interventions;
DROP TABLE IF EXISTS patient_encounters;

CREATE TABLE patient_encounters (
    encounter_id INT PRIMARY KEY,
    patient_nbr INT,
    age VARCHAR(50),
    time_in_hospital INT,
    number_inpatient INT,
    number_emergency INT,
    number_outpatient INT,
    num_medications INT,
    num_lab_procedures INT,
    discharge_disposition_id INT,
    admission_type_id INT,
    readmitted VARCHAR(20),
    risk_score INT,
    risk_level VARCHAR(20)
);

CREATE TABLE care_interventions (
    intervention_id SERIAL PRIMARY KEY,
    encounter_id INT REFERENCES patient_encounters(encounter_id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'PENDING_REVIEW',
    assigned_to VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);