# import json
# from pathlib import Path

# # 1. Get the path to repository.py, then go up TWO parents to reach the Day3 project root
# BASE_DIR = Path(__file__).parent.parent

# # 2. Point to your targets inside the data folder
# DATA_FILE_JSON = BASE_DIR / "data" / "invoices_data.json"
# DATA_FILE_CSV = BASE_DIR / "data" / "homework_invoices.csv"
# DATA_FILE = "../../data/invoices_data.json"
# def load_json_data():
#     """Safely loads and returns the JSON invoice data."""
#     with open(DATA_FILE_JSON, "r") as f:
#         return json.load(f)

# # You can use this variable to access your data directly
# invoices = load_json_data()
payments_db = [
    {"invoice_id": "INV-101", "paid": 85000},
    {"invoice_id": "INV-101", "paid": 85000},
    {"invoice_id": "INV-104", "paid": 60000},
    {"invoice_id": "INV-109", "paid": 12000},
]

def get_all_payments():
    return payments_db

def get_payments_by_invoice_id(invoice_id: str):
    # Returns all payment records matching this invoice_id
    matches = [p for p in payments_db if p["invoice_id"] == invoice_id]
    return matches

def add_payment(payment_data: dict):
    payments_db.append(payment_data)
    return payment_data

def update_payment_by_invoice(invoice_id: str, updated_data: dict):
    # Updates the first matching payment for this invoice_id
    for p in payments_db:
        if p["invoice_id"] == invoice_id:
            if updated_data.get("paid") is not None:
                p["paid"] = updated_data["paid"]
            return p
    return None

def delete_payments_by_invoice(invoice_id: str):
    # Deletes all payments associated with this invoice_id
    global payments_db
    initial_len = len(payments_db)
    payments_db = [p for p in payments_db if p["invoice_id"] != invoice_id]
    deleted_count = initial_len - len(payments_db)
    return deleted_count > 0