import json
from collections import defaultdict
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "invoices_data.json"

with open(DATA_FILE) as f:
    invoices = json.load(f)

vendor_totals = {}
invoice_positions = defaultdict(list)

for index, invoice in enumerate(invoices):
    vendor = invoice["vendor"]
    amount = invoice["amount"]
    vendor_totals[vendor] = (vendor_totals.get(vendor,0)+amount)
    inv_id = invoice.get("invoice_id") or invoice.get("id")
    
    # If the file contains an invoice without any ID, skip it safely
    if inv_id:
        invoice_positions[inv_id].append(index)

for vendor,total in vendor_totals.items():
    print (vendor,total)

seen = set()

duplicates = []
print("\n--- Duplicate Positions ---")
for inv_id, idx_list in invoice_positions.items():
    if len(idx_list) > 1:
        print(f"{inv_id} -> {idx_list}")