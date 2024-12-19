from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime

# from Emails.SendEmailReplacementsOneTime import send_email_replacement_onetime, send_email_replacement_onetime_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_solve(data):
    # Get parameters
    replacement_id = data.get("replacement_id")
    teacher_id = data.get("teacher_id")
    if not replacement_id:
        return {"data": {"response": "Replacement ID is required", "status": 400}}

    # Initialize the Salesforce client
    sf = getSF()

    # Update the replacement
    sf.sf.Replacement__c.update(replacement_id, { "Teacher__c": teacher_id })

    return {"data": {"response": "Success", "status": 200}}
