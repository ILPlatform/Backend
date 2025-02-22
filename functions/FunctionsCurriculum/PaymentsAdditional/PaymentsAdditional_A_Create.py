from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_additional_a_create(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all payments from SF
    details = data.get("details")
    details["RecordTypeId"] = "012P5000001tcX7IAI"

    # Create the payment
    payment = safe_create(sf.sf.Payment__c, details)

    # Return the payment ID
    return {"data": {"response": {"Id": payment.get("id")}, "status": 200}}
