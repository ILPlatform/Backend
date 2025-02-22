from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def classes_a_update_names(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the user
    results = sf.sf.query_all_iter(f"""
        SELECT Id, Code__c
        FROM Opportunity
        WHERE RecordTypeId = '012060000003OPWAA2'
    """)

    # Bulk update the names to match the codes
    sf.sf.bulk.Opportunity.update([
        {'Id': result.get("Id"), "Name": result.get("Code__c")} for result in results
    ])

    return {"data": {"response": "Success", "status": 200}}
