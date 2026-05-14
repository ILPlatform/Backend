from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom, safe_query
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def users_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all users from SF
    sf_results = safe_query(sf, """
        SELECT FIELDS(ALL)
        FROM Employee__c
    """)

    # Get all users from Firebase
    firebase_results = [{
        "uid": user.uid,
        "claims": user.custom_claims,
        "roles": user.custom_claims.get("roles") if user.custom_claims else None,
        "last_sign_in": user.user_metadata.last_sign_in_timestamp
    } for user in auth.list_users().iterate_all()]

    # Link the user data
    def get_firebase_user(sf_user):
        for firebase_user in firebase_results:
            if sf_user.get("Firebase_UID__c") == firebase_user.get("uid"):
                return firebase_user
        return {}

    # Process joint data
    def get_user_data(sf_user):
        firebase_user = get_firebase_user(sf_user)
        return sf_user | {
            "id": sf_user.get("Id"),
            "uid": firebase_user.get("uid"),
            "email": sf_user.get("Email__c"),
            "name": sf_user.get("Full_Name__c"),
            "claims": firebase_user.get("claims"),
            "roles": firebase_user.get("roles"),
            "phone": sf_user.get("Phone__c").replace("+", "").replace(" ", "") if sf_user.get("Phone__c") else None,
            "last_sign_in": firebase_user.get("last_sign_in"),
            "image_url": sf_user.get("Image_URL__c"),
            "criminal": sf_user.get("Criminal_Record__c")
        }

    return {"data": {"response": list(map(get_user_data, sf_results)), "status": 200}}
