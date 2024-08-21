# Function to update a document by joining its signed version. Requires authentication.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def docs_u_update_signed(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    uid = data.get("uid")
    document_id = data.get("document_id")
    signed_url = data.get("signed_url")
    if not document_id:
        return {"data": {"response": "Document ID are required"}, "status": 404}

    document = sf.sf.Document__c.get(document_id)

    if not document:
        return {"data": {"response": "Document not found", "status": 404}}

    if document.get("To_Sign__c") and not signed_url:
        return {"data": {"response": "Signed URL is required when signature is required", "status": 400}}

    # Update the contract
    timestamp = datetime.now().strftime("%Y-%m-%d"+"T"+"%H:%M:%S"+"Z")
    sf.sf.Document__c.update(document_id, { "Signed__c": True, "Signed_URL__c": signed_url, "Signed_Timestamp__c":  timestamp})

    return {"data": {"response": "Successfully Signed Contract", "status": 200}}
