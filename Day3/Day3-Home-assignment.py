invoices = [
    {"invoice_id": "INV-101", "vendor": "ABC Ltd", "amount": 85000, "status": "PENDING", "date": "2026-09-03"},
    {"invoice_id": "INV-102", "vendor": "xyz corp", "amount": 142500, "status": "pending", "date": "2026-09-05"},
    {"invoice_id": "INV-101", "vendor": "ABC Ltd", "amount": 85000, "status": "PENDING", "date": "2026-09-03"},
    {"invoice_id": "INV-103", "vendor": "Globex", "amount": -550000, "status": "PENDING", "date": "2026-09-07"},
    {"invoice_id": "INV-104", "vendor": "ABC Ltd ", "amount": 62000, "status": "PAID", "date": "2026-09-08"},
    {"invoice_id": "INV-102", "vendor": "XYZ Corp", "amount": 150000, "status": "PENDING", "date": "2026-09-12"},
    {"invoice_id": "INV-105", "vendor": "Globex", "amount": 550000, "status": "PENDING", "date": "2026-09-09"},
    {"invoice_id": "INV-106", "vendor": "Initech", "amount": None, "status": "PENDING", "date": "2026-09-15"},
    {"invoice_id": "INV-107", "vendor": "ABC Ltd", "amount": 85000, "status": "PENDING", "date": "2026-09-03"},
]

payments = [
    {"invoice_id": "INV-101", "paid": 85000},
    {"invoice_id": "INV-101", "paid": 85000},
    {"invoice_id": "INV-104", "paid": 60000},
    {"invoice_id": "INV-109", "paid": 12000},
]

# --- Task 1: Normalize & Report None Amounts ---
print("=== TASK 1: NORMALIZATION ===")
for i in range(len(invoices)):
    if invoices[i]["vendor"]:
        invoices[i]["vendor"] = invoices[i]["vendor"].strip().title()
    if invoices[i]["status"]:
        invoices[i]["status"] = invoices[i]["status"].upper()
    if invoices[i]["amount"] is None:
        print(f"Row {i} has amount as None: {invoices[i]}")

# --- Task 2: Exact Duplicates ---
print("\n=== TASK 2: EXACT DUPLICATES ===")
exact_dupes = {}
seen = {}
to_remove = set()

for i, inv in enumerate(invoices):
    # Create a tuple representing all fields
    key = (inv["invoice_id"], inv["vendor"], inv["amount"], inv["status"], inv["date"])
    if key in seen:
        if key not in exact_dupes:
            exact_dupes[key] = [seen[key]]
        exact_dupes[key].append(i)
        to_remove.add(i)
    else:
        seen[key] = i

print("Exact dupes mapping:", exact_dupes)

# Remove exact duplicates iterating backwards to preserve indices
for i in sorted(list(to_remove), reverse=True):
    invoices.pop(i)


# --- Task 3: Suspected Duplicates ---
print("\n=== TASK 3: SUSPECTED DUPLICATES ===")
# Match on vendor, amount, and date but different invoice_id
for i in range(len(invoices)):
    for j in range(i + 1, len(invoices)):
        inv1, inv2 = invoices[i], invoices[j]
        if (
            inv1["vendor"] == inv2["vendor"]
            and inv1["amount"] == inv2["amount"]
            and inv1["date"] == inv2["date"]
            and inv1["invoice_id"] != inv2["invoice_id"]
            and inv1["amount"] is not None
        ):
            print(f"Suspected Duplicate Pair: ({inv1['invoice_id']} ~ {inv2['invoice_id']})")


# --- Task 4: Credit Notes ---
print("\n=== TASK 4: CREDIT NOTES ===")
for i, inv in enumerate(invoices):
    if inv["amount"] is not None and inv["amount"] < 0:
        abs_amount = abs(inv["amount"])
        partner_found = False
        for j in range(i):
            prev_inv = invoices[j]
            if (
                prev_inv["vendor"] == inv["vendor"]
                and prev_inv["amount"] == abs_amount
                and prev_inv["status"] != "CANCELLED"
            ):
                prev_inv["status"] = "CANCELLED"
                inv["status"] = "CANCELLED"
                print(f"Credit Note Match Index Pair: {j} <-> {i} ({prev_inv['invoice_id']} & {inv['invoice_id']})")
                partner_found = True
                break
        if not partner_found:
            print(f"Unmatched Credit Note at index {i}: {inv['invoice_id']}")


# --- Task 5: Reconcile Payments ---
print("\n=== TASK 5: PAYMENT RECONCILIATION ===")
payment_totals = {}
for p in payments:
    inv_id = p["invoice_id"]
    payment_totals[inv_id] = payment_totals.get(inv_id, 0) + p["paid"]

valid_invoices = {inv["invoice_id"]: inv for inv in invoices if inv["amount"] is not None and inv["status"] != "CANCELLED"}

for inv_id, total_paid in payment_totals.items():
    if inv_id in valid_invoices:
        print(f"Invoice {inv_id}: Total Paid = ${total_paid}")
    else:
        print(f"Payment for Unknown/Cancelled Invoice {inv_id}: Total Paid = ${total_paid} (Unmatched)")