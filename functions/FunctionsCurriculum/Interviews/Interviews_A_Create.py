from Helpers import firebase_functions_custom, https_fn_custom, safe_create
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

    # Create the note in Salesforce
    note = safe_create(sf.sf.Note__c, details | {"RecordTypeId": "012P5000001UtMf"})

    return {"data": {"response": {"Id": note.get("id")}, "status": 200}}
