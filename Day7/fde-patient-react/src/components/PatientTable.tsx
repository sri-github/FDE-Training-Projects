import type { Encounter } from '../types';
import PatientRow from './patientrow';

interface PatientTableProps {
  encounters: Encounter[];
}

export default function PatientTable({ encounters }: PatientTableProps) {
  if (!encounters || encounters.length === 0) {
    return <p className="no-data">No patient encounters available.</p>;
  }

  return (
    <table className="patient-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Patient Name</th>
          <th>Age</th>
          <th>Condition</th>
        </tr>
      </thead>
      <tbody>
        {encounters.map((encounter) => (
          <PatientRow key={encounter.encounter_id} encounter={encounter} />
        ))}
      </tbody>
    </table>
  );
}