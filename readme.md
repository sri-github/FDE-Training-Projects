# Persistent Invoice API (FastAPI & JSON)

## Overview
A persistent FastAPI-based invoice management application that stores data in a JSON file (`data/invoices.json`) to ensure records survive server restarts[cite: 2].

## Project Structure
- `main.py`: Contains FastAPI application routes (`GET`, `POST`, `PUT`, `DELETE`) and JSON file handling logic.
- `models.py`: Defines the Pydantic data models (`Invoice`).
- `data/invoices.json`: JSON file acting as the persistence storage layer.

## Endpoints
- **GET /invoices**: Retrieves all invoice records from `invoices.json`[cite: 3].
- **GET /invoices/{invoice_id}**: Retrieves a single invoice by ID or returns a `404` error[cite: 5].
- **POST /invoices**: Creates a new invoice, saves it to the JSON file, and returns a `201` status[cite: 5].
- **PUT /invoices/{invoice_id}**: Updates an existing invoice and persists the changes.
- **DELETE /invoices/{invoice_id}**: Removes an invoice by ID and updates the JSON file[cite: 5].

## How to Run
1. Navigate to the `Day2` directory:
   ```bash
   cd Day2

## Sample test run
(.venv) FDE-Training-Projects> python Day3/Day3-Home-assignment.py
=== TASK 1: NORMALIZATION ===
Row 7 has amount as None: {'invoice_id': 'INV-106', 'vendor': 'Initech', 'amount': None, 'status': 'PENDING', 'date': '2026-09-15'}

=== TASK 2: EXACT DUPLICATES ===
Exact dupes mapping: {('INV-101', 'Abc Ltd', 85000, 'PENDING', '2026-09-03'): [0, 2]}

=== TASK 3: SUSPECTED DUPLICATES ===
Suspected Duplicate Pair: (INV-101 ~ INV-107)

=== TASK 4: CREDIT NOTES ===
Unmatched Credit Note at index 2: INV-103

=== TASK 5: PAYMENT RECONCILIATION ===
Invoice INV-101: Total Paid = $170000
Invoice INV-104: Total Paid = $60000
Payment for Unknown/Cancelled Invoice INV-109: Total Paid = $12000 (Unmatched)
(.venv) FDE-Training-Projects> 
