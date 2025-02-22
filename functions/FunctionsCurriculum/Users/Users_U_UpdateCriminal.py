from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import firestore
from Salesforce import getSF
from Emails import send_email_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def users_u_update_criminal(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    user_id = data.get("user_id")
    criminal_url = data.get("criminal_url")

    if not user_id or not criminal_url:
        return {"data": {"response": "User UID and Criminal url are required", "status": 400}}

    # Update the user in Salesforce
    sf.sf.Employee__c.update(user_id, {"Criminal_Record__c": criminal_url})

    return {"data": {"response": "User updated successfully", "status": 200}}
