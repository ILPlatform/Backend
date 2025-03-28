from Helpers import firebase_functions_custom, https_fn_custom, safe_update
from Salesforce import getSF
from Emails import sendEmail

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_a_update(data):
    # Initialize SF
    sf = getSF()

    # Create the replacement
    details = data.get("details")
    safe_update(sf.sf.Replacement__c, details)
    #
    # # Send email to admins
    # sendEmail("replacement_admin", details)

    return {"data": {"response": "Success", "status": 200}}
