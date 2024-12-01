from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_a_mark_paid(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    payment_id = data.get("payment_id")

    print(data)

    # Update the payment in SF
    sf.sf.Payment__c.update(payment_id, {"Paid__c": True})

    return {"data": {"response": 1, "status": 200}}
