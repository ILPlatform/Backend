# Function to update a document by joining its signed version. Requires authentication.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def docs_U_update_signed(data):
    # Initialize DB and SF
    db = firestore.client()

    # Get the parameters
    uid = data.get("uid")
    document_id = data.get("document_id")
    signed_url = data.get("signed_url")
    if not document_id:
        return {"data": {"response": "Document ID are required"}, "status": 404}

    # Get all contracts of the given user
    contract_doc = db.collection("Documents").document(document_id)
    contract_data = contract_doc.get()
    if not contract_data.exists:
        return {"data": {"response": "Document not found", "status": 404}}

    contract = contract_data.to_dict() or {}

    if contract.get("to_sign") and not signed_url:
        return {"data": {"response": "Signed URL is required when signature is required", "status": 400}}

    # Update the contract
    contract["signed"] = True
    contract["signed_timestamp"] = firestore.SERVER_TIMESTAMP
    contract["signed_url"] = signed_url
    contract_doc.set(contract)

    return {"data": {"response": "Successfully Signed Contract", "status": 200}}
