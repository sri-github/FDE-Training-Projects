import { useState, useEffect } from 'react';
import type { Encounter } from '../types';

export function usePaginatedFetch(page: number, limit: number = 10) {
  const [encounters, setEncounters] = useState<Encounter[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const skip = (page - 1) * limit;
    setLoading(true);

    // FIX: Updated to match your backend route /api/queue from main.py
    fetch(`http://localhost:8000/api/queue?limit=${limit}`)
      .then((response) => {
        if (!response.ok) throw new Error('Failed to fetch encounters');
        return response.json();
      })
      .then((data) => {
        setEncounters(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [page, limit]);

  return { encounters, loading, error };
}