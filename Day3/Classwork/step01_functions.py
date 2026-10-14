def determine_approval(invoice_amount):
    if invoice_amount > 10000:
        return "Manager Approval required"
    elif invoice_amount > 500:
        return "Supervisor approval required"
    else:
        return "Standard approval required"


approver = determine_approval(1200)
print(approver)