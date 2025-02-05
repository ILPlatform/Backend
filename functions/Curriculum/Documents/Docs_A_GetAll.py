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
        SELECT FIELDS(ALL), Teacher__r.Name
        FROM Document__c
        WHERE Deleted__c = False
        LIMIT 200
        """)

    # Process the contracts
    # return_value = [{
    #     "id": document.get("Id"),
    #     "employee_id": document.get("Teacher__r", {}).get("Id") if document.get("Teacher__r") else None,
    #     "uid": document.get("Teacher__r", {}).get("Firebase_UID__c") if document.get("Teacher__r") else None,
    #     # "name": document.get("Teacher__r", {}).get("Name") if document.get("Teacher__r") else None,
    #     "CreatedDate": document.get("CreatedDate"),
    #     "Description__c": document.get("Description__c"),
    #     "signed": document.get("Signed__c"),
    #     "url": document.get("Unsigned_URL__c"),
    #     "signed_url": document.get("Signed_URL__c"),
    #     "Signed_Timestamp__c": document.get("Signed_Timestamp__c"),
    #     "to_sign": document.get("To_Sign__c"),
    # } for document in documents]

    return {"data": {"response": list(documents), "status": 200}}
