interface Encounter {
    encounter_id: number;
    patient_id: number;
    risk_score: number;
    risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
}

const encounterQueue: Encounter[] = [
    {encounter_id: 101, patient_id: 2001,risk_score:85, risk_level:'HIGH'},
    {encounter_id: 102, patient_id: 2002,risk_score:85, risk_level:'MEDIUM'}
]

console.log(encounterQueue);
console.log('api logs');
console.log(JSON.stringify(encounterQueue,null,2))