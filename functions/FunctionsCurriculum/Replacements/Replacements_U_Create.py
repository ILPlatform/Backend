from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF
from Emails import sendEmail

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def replacements_u_create(data):
    # Initialize SF
    sf = getSF()

    # Create the replacement
    details = data.get("details")
    user_details = data.get("user_details")
    replacement = safe_create(sf.sf.Replacement__c, details | {
        "Teacher_Old__c": user_details.get("Id")
    })

    # Send email to admins
    sendEmail("replacement_admin", details)

    return {"data": {"response": {"Id": replacement.get("id")}, "status": 200}}
