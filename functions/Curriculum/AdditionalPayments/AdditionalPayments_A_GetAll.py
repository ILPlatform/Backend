from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def additional_payments_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all payments from SF
    sf_results = list(sf.sf.query_all_iter(f"""
        SELECT FIELDS(ALL), Beneficiary__r.Full_Name__c
        FROM Payment__c
        WHERE (RecordTypeId = '012P5000001tcX7IAI' OR RecordTypeId = NULL)
            AND Deleted__c = False
        LIMIT 200
    """))

    return {"data": {"response": sf_results, "status": 200}}
