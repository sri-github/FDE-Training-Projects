interface EncounterUIModel {
    encounter_id: number;
    patient_nbr: number;
    age: string;
    time_in_hospital: number;
    risk_score: number;
    risk_level: string;
    readmitted: string;
}

interface DashboardStats {
    total_encounters: number;
    high_risk_count: number;
    pending_interventions: number;
}

async function fetchDashboardStats() {
    try {
        console.log("Fetching Dashboard Statistics...");
        const response = await fetch("http://localhost:8000/api/stats");
        if (!response.ok) {
            throw new Error(`HTTP Error. Status: ${response.status}`);
        }
        const stats: DashboardStats = await response.json();
        console.log("\n========================================");
        console.log("       DASHBOARD QUEUE STATISTICS       ");
        console.log("========================================");
        console.log(`- Total Encounters      : ${stats.total_encounters}`);
        console.log(`- High-Risk Patients    : ${stats.high_risk_count}`);
        console.log(`- Pending Interventions : ${stats.pending_interventions}`);
        console.log("========================================\n");
    } catch (error) {
        console.error("Failed to fetch stats:", error);
    }
}

async function fetchHighRiskQueueSummary() {
    try {
        console.log("Fetching top high-risk encounter queue (Limited to 5)...");
        // Limiting to 5 so it doesn't flood the console
        const response = await fetch("http://localhost:8000/api/queue/high-risk?limit=2");
        if (!response.ok) {
            throw new Error(`HTTP Error. Status: ${response.status}`);
        }
        const encounters: EncounterUIModel[] = await response.json();
        console.log(`\n=== High-Risk Queue Preview (${encounters.length} records shown) ===`);
        console.log(JSON.stringify(encounters, null, 2));
    } catch (error) {
        console.error("Failed to connect to FastAPI", error);
    }
}

async function runHomeworkClient() {
    await fetchHighRiskQueueSummary();
    await fetchDashboardStats();
}

runHomeworkClient();