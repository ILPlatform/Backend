# Function to delete a document from the database. Requires document admin level.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_delete(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    document = data.get('details')
    if not document or not document.get("Id"):
        return {"data": {"response": "Document ID is required", "status": 400}}

    # Create a document in the database
    sf.sf.Document__c.update(document.get("Id"), {"Deleted__c": True})

    return {"data": {"response": "Success", "status": 200}}
