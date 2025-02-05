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
    payment = data.get("details")
    payment.update({
        "RecordTypeId": "012P5000001tcX7IAI"
    })

    # Create the payment
    payment = sf.sf.Payment__c.create(payment)

    # Return the payment ID
    return {"data": {"response": {"Id": payment.get("id")}, "status": 200}}
