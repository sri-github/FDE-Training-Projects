import { useState } from 'react';
import Header from './components/header';
import PatientTable from './components/PatientTable';
import Pagination from './components/Pagination';
import { usePaginatedFetch } from './hooks/usePaginationFetch';
import './App.css';

function App() {
  const [page, setPage] = useState<number>(1);
  const { encounters, loading, error } = usePaginatedFetch(page, 10);

  return (
    <div className="App">
      <Header />
      <main className="p-6">
        {loading && <p>Loading clinical records...</p>}
        {error && <p className="text-red-500">Error: {error}</p>}
        {!loading && !error && <PatientTable encounters={encounters} />}
        
        <Pagination page={page} setPage={setPage} />
      </main>
    </div>
  );
}

export default App;