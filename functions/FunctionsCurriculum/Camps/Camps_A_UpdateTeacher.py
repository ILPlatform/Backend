from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def camps_a_update_teacher(data):
    # Get parameters
    camp_id = data.get("camp_id")
    teacher_id = data.get("teacher_id")

    # Initialize DB and SF
    sf = getSF()

    # Bulk update the names to match the codes
    sf.sf.Opportunity.update(camp_id, {"Teacher__c": teacher_id})

    return {"data": {"response": "Success", "status": 200}}
