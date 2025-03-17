from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF
from Emails import sendEmail

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_a_create(data):
    # Initialize SF
    sf = getSF()

    # Create the replacement
    details = data.get("details")
    replacement = safe_create(sf.sf.Replacement__c, details)

    # Send email to admins
    sendEmail("replacement_admin", details)

    return {"data": {"response": {"Id": replacement.get("id")}, "status": 200}}
