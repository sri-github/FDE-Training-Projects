interface PaginationProps {
  page: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
}

export default function Pagination({ page, setPage }: PaginationProps) {
  return (
    <div className="pagination-controls" style={{ marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <button 
        onClick={() => setPage((prev) => Math.max(prev - 1, 1))} 
        disabled={page === 1}
      >
        Previous
      </button>
      
      <span>Page {page}</span>
      
      <button 
        onClick={() => setPage((prev) => prev + 1)}
      >
        Next
      </button>
    </div>
  );
}