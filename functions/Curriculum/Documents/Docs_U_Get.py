# Function to get all documents related to an authenticated user. Requires authentication.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore, auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def docs_u_get(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    uid = data.get("uid")

    # Get all contracts from Salesforce
    contracts = sf.sf.query_all_iter(f"""
        SELECT
            Id, CreatedDate,
            Description__c, Signed__c, Unsigned_URL__c, Signed_URL__c, Type__c, Deleted__c, To_Sign__c
        FROM Document__c
        WHERE Teacher__r.Firebase_UID__c = '{uid}'
            AND Deleted__c = False
        """)

    # Process the contracts
    return_value = [{
        "id": contract.get("Id"),
        "timestamp": contract.get("CreatedDate"),
        "description": contract.get("Description__c"),
        "signed": contract.get("Signed__c"),
        "url": contract.get("Unsigned_URL__c"),
        "signed_url": contract.get("Signed_URL__c"),
        "to_sign": contract.get("To_Sign__c"),
    } for contract in contracts]

    return {"data": {"response": return_value, "status": 200}}
