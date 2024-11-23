

from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime

# from Emails.SendEmailReplacementsOneTime import send_email_replacement_onetime, send_email_replacement_onetime_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_delete(data):
    # Get the parameters
    replacement_id = data.get("id")

    # Initialize the Salesforce client
    sf = getSF()

    try:
        # Delete the one-time replacements
        sf.sf.Replacement__c.update(replacement_id, {"Deleted__c": True})
    except Exception as e:
        return {"data": {"response": f"Error deleting replacement: {e}", "status": 400}}

    return {"data": {"response": "Success", "status": 200}}
