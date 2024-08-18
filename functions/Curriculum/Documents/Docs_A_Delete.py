# Function to delete a document from the database. Requires document admin level.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_A_delete(data):
    # Initialize DB and SF
    db = firestore.client()

    # Get the parameters
    document_id = data.get('document_id')

    if not document_id:
        return {"data": {"response": "Document UID is required", "status": 400}}

    # Create a document in the database
    db.collection("Documents").document(document_id).update({
        "deleted": True
    })

    return {"data": {"response": "Success", "status": 200}}
