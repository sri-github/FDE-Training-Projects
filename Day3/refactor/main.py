from fastapi import FastAPI, HTTPException
from typing import List
from models import Payment, PaymentUpdate
import repository

app = FastAPI(title="Payments Management API", version="1.0.0")

@app.get("/payments", response_model=List[dict])
def list_payments():
    return repository.get_all_payments()

@app.get("/payments/{invoice_id}", response_model=List[dict])
def get_payments_for_invoice(invoice_id: str):
    payments = repository.get_payments_by_invoice_id(invoice_id)
    if not payments:
        raise HTTPException(status_code=404, detail=f"No payments found for invoice ID {invoice_id}.")
    return payments

@app.post("/payments", response_model=dict, status_code=201)
def create_payment(payment: Payment):
    return repository.add_payment(payment.dict())

@app.put("/payments/{invoice_id}", response_model=dict)
def update_existing_payment(invoice_id: str, payment_update: PaymentUpdate):
    updated = repository.update_payment_by_invoice(invoice_id, payment_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Payment for invoice ID {invoice_id} not found.")
    return updated

@app.delete("/payments/{invoice_id}")
def remove_payments_for_invoice(invoice_id: str):
    success = repository.delete_payments_by_invoice(invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"No payments found to delete for invoice ID {invoice_id}.")
    return {"detail": f"Payments for invoice {invoice_id} deleted successfully."}