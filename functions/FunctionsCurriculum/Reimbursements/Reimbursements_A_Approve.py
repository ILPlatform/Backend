from datetime import datetime

from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF


@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def reimbursements_a_approve(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all payments from SF
    details = data.get("details", {})

    # Create the payment
    payment = safe_create(sf.sf.Payment__c, {
        "RecordTypeId": "012P5000001tcX7IAI",
        "Beneficiary__c": details.get("Employee__r", {}).get("Id", ""),
        "Name": "Remboursement " + details.get("Name", ""),
        "Amount__c": details.get("Amount__c", 0),
        "Month__c": datetime.now().month,
        "Year__c": datetime.now().year
    })

    # Update the reimbursement status to "Accepted"
    sf.sf.Reimbursement__c.update(details.get("Id", ""), {
        "Status__c": "Accepted"
    })

    # Return the payment ID
    return {"data": {"response": {"Id": payment.get("id")}, "status": 200}}
