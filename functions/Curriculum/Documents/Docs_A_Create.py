# Function to create a new document in the database. Requires document admin level.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from Emails import send_email_new_document
from firebase_admin import firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_A_create(data):
    # Initialize DB and SF
    db = firestore.client()
    sf = getSF()

    # Get the parameters
    user_uid = data.get("user_uid")
    url = data.get("url")
    to_sign = data.get("to_sign")
    type = data.get("type")
    year = data.get("year")
    month = data.get("month")

    if not user_uid:
        return {"data": {"response": "User UID is required", "status": 400}}
    if not url or not type or not year or not month:
        return {"data": {"response": "URL, to_sign, type, year and month are required", "status": 400}}

    # Get the user's name from SF
    result = sf.sf.query(f"SELECT Full_Name__c, Email__c FROM Employee__c WHERE Firebase_UID__c = '{user_uid}'")
    if not result["records"]:
        return {"data": {"response": "User not found", "status": 400}}
    user_name = result["records"][0].get("Full_Name__c")
    user_email = result["records"][0].get("Email__c")

    # Create a document in the database
    db.collection("Documents").add({
        "timestamp": firestore.SERVER_TIMESTAMP,
        "uid": user_uid,
        "name": user_name,
        "url": url,
        "to_sign": to_sign,
        "type": type,
        "year": year,
        "month": month,
        "description": f"{type} {year}/{month}",
        "signed": False
    })

    # Send email to the user
    send_email_new_document(user_email, f"{type} {year}/{month}")

    return {"data": {"response": "Success", "status": 200}}
