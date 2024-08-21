# Function to get all the documents from the database. Requires document admin level.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import auth, firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all contracts
    documents = sf.sf.query_all_iter(f"""
        SELECT
            Id, CreatedDate,
            Description__c, Signed__c, Unsigned_URL__c, Signed_URL__c, Type__c, Deleted__c, To_Sign__c, Signed_Timestamp__c,
            Teacher__r.Name, Teacher__r.Firebase_UID__c
        FROM Document__c
        WHERE Deleted__c = False
        """)

    # Process the contracts
    return_value = [{
        "id": document.get("Id"),
        "uid": document.get("Teacher__r", {}).get("Firebase_UID__c") if document.get("Teacher__r") else None,
        "name": document.get("Teacher__r", {}).get("Name") if document.get("Teacher__r") else None,
        "timestamp": document.get("CreatedDate"),
        "description": document.get("Description__c"),
        "signed": document.get("Signed__c"),
        "url": document.get("Unsigned_URL__c"),
        "signed_url": document.get("Signed_URL__c"),
        "signed_timestamp": document.get("Signed_Timestamp__c"),
        "to_sign": document.get("To_Sign__c"),
    } for document in documents]

    return {"data": {"response": return_value, "status": 200}}
