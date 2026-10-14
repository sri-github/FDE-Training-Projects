invoices=[
    {
        "invoice_id":"INV_001",
        "vendor":"ABC Ltd",
        "amount":1500.0,
        "status":"Paid"
    },
    {
        "invoice_id":"INV_002",
        "vendor":"XYZ Ltd",
        "amount":500.0,
        "status":"Paid"
    }
]

for index, invoice in enumerate(invoices):
    if invoice["invoice_id"] == "INV_001":
        invoices[index]["invoice_id"]="INV_003"
    print(index,invoice)