from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_a_create(data):
    # Initialize SF
    sf = getSF()

    # Get all payments from SF
    details = data.get("details")
    details["RecordTypeId"] = "012P5000001tRevIAE"

    # Create the payment
    payment = safe_create(sf.sf.Payment__c, details)

    # Return the payment ID
    return {"data": {"response": {"Id": payment.get("id")}, "status": 200}}
