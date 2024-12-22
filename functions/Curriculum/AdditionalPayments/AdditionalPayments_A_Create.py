from firebase_functions.private.util import P
from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def additional_payments_a_create(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all payments from SF
    sf_data = {
        "Amount__c": data.get("amount"),
        "Year__c": data.get("year"),
        "Month__c": data.get("month"),
        "Name": data.get("description"),
        "Beneficiary__c": data.get("beneficiary_id"),
        "RecordTypeId": "012P5000001tcX7IAI"
    }

    # Create the payment
    sf.sf.Payment__c.create(sf_data)

    return {"data": {"response": "Success", "status": 200}}
