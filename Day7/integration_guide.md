# Project Setup, Execution Commands & Integration Guide

This document serves as the single source of truth for running both the FastAPI backend and React frontend applications, including file locations, startup commands, and resolved integration fixes.

---

## 1. Project Directory Overview

```text
FDE-Training-Projects/
├── Day4/                             <-- Backend Root Directory
│   ├── data/
│   │   └── diabetic_data.csv
│   └── refactor/                     <-- Python Package Directory
│       ├── database.py
│       ├── load_data.py
│       ├── main.py                    <-- FastAPI App Entry Point
│       ├── models.py
│       ├── repository.py
│       └── services.py
└── Day7/
    └── fde-patient-react/            <-- React Frontend Directory
        ├── src/
        │   ├── components/
        │   │   ├── Header.tsx
        │   │   ├── Pagination.tsx
        │   │   ├── PatientRow.tsx
        │   │   └── PatientTable.tsx
        │   ├── hooks/
        │   │   └── usePaginationFetch.ts
        │   ├── App.tsx
        │   ├── main.tsx
        │   └── types.ts
        └── package.json
```

---

## 2. Startup Instructions & Commands

### A. Running the FastAPI Backend

1. Open a terminal window in your IDE or system terminal.
2. Navigate to the **`Day4`** directory (parent folder of `refactor`):
   ```bash
   cd "D:\ML and QA AI\Test Leaf FDE\FDE-Training-Projects\Day4"
   ```
3. Ensure your Python virtual environment (`.venv`) is activated.
4. Run Uvicorn referencing the `refactor` package path:
   ```bash
   uvicorn refactor.main:app --reload
   ```
   * **Backend URL**: `http://localhost:8000`
   * **Swagger Interactive Docs**: `http://localhost:8000/docs`

> **Note on Relative Import Error**: Running `uvicorn main:app` directly inside `Day4/refactor` causes `ImportError: attempted relative import with no known parent package`. Always run `uvicorn refactor.main:app` from the `Day4` directory.

---

### B. Running the React Frontend

1. Open a **second** terminal window.
2. Navigate to the React project directory:
   ```bash
   cd "D:\ML and QA AI\Test Leaf FDE\FDE-Training-Projects\Day7\fde-patient-react"
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   * **Frontend URL**: `http://localhost:5173`

---

## 3. Key Issues Resolved & Final Code Reference

### Issue 1: Route Mismatch (404 Not Found)
* **Problem**: Frontend fetch was hitting `http://localhost:8000/encounters`.
* **Fix**: Backend `refactor/main.py` defines `@app.get("/api/queue")`. Update `usePaginationFetch.ts` to hit `/api/queue`.

### Issue 2: Cross-Origin Resource Sharing (CORS Error)
* **Problem**: Browser blocked requests from `localhost:5173` to `localhost:8000`.
* **Fix**: Added `CORSMiddleware` in `Day4/refactor/main.py`.

---

### Key File Configurations

#### 1. Backend CORS Middleware (`Day4/refactor/main.py`)
```python
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .repository import *
from .services import *
from .models import *
from .database import *

app = FastAPI(title="Diabetes Readmission Intervention Queue", version="1.0")

# CORS Middleware unblocks React frontend requests from localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/queue", response_model=List[PatientEncounter])
def get_queue(limit: int = 50):
    try:
        return fetch_patient_queue(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# (Rest of existing endpoints remain unchanged)
```

#### 2. Frontend Fetch Hook (`Day7/fde-patient-react/src/hooks/usePaginationFetch.ts`)
```typescript
import { useState, useEffect } from 'react';
import type { Encounter } from '../types';

export function usePaginatedFetch(page: number, limit: number = 10) {
  const [encounters, setEncounters] = useState<Encounter[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const skip = (page - 1) * limit;
    setLoading(true);

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
```

---

## 4. Quick Checklist Before Development
- [ ] Terminal 1: Inside `Day4` → Run `uvicorn refactor.main:app --reload`
- [ ] Terminal 2: Inside `fde-patient-react` → Run `npm run dev`
- [ ] Check API Docs at `http://localhost:8000/docs`
- [ ] Open App at `http://localhost:5173`