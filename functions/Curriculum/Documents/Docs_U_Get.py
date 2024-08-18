# Function to get all documents related to an authenticated user. Requires authentication.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore, auth

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def docs_U_get(data):
    # Initialize DB and SF
    db = firestore.client()

    # Get the parameters
    uid = data.get("uid")

    # Get all contracts of the given user
    contracts = db.collection("Documents").where(filter=FieldFilter("uid", "==", uid)).order_by("timestamp", "DESCENDING").stream()

    # Process the contracts
    return_value = []
    for contract in contracts:
        contract_dict = contract.to_dict()
        if contract_dict.get("deleted"):
            continue

        return_value.append({
            "id": contract.id,
            "timestamp": contract_dict.get("timestamp"),
            "description": contract_dict.get("description"),
            "signed": contract_dict.get("signed"),
            "url": contract_dict.get("url"),
            "signed_url": contract_dict.get("signed_url"),
            "to_sign": contract_dict.get("to_sign"),
        })


    return {"data": {"response": return_value, "status": 200}}
