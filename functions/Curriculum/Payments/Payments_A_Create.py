from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=4)
def payments_a_create(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters
    details = data.get("details")
    if not details:
        return {"data": {"response": "Details are required", "status": 400}}

    # Add RecordTypeId to details
    details["RecordTypeId"] = "012P5000001tRevIAE"

    # Create the user in Salesforce
    payment = safe_create(sf.sf.Payment__c, details)

    return {"data": {"response": {"Id": payment.get("id")}, "status": 200}}
