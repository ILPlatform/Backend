from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=4)
def interviews_a_create(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters
    details = data.get("details")
    if not details:
        return {"data": {"response": "User details are required", "status": 400}}

    # Add RecordTypeId to details
    details["RecordTypeId"] = "012P5000001UtMf"

    # Create the user in Salesforce
    sf.sf.Note__c.create(details)

    return {"data": {"response": "Note created successfully", "status": 200}}
