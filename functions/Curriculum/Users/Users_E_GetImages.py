from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=0)
def users_e_get_images(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all users from SF
    sf_results = sf.sf.query_all_iter(f"""
        SELECT
            Id, Name, Image_URL__c
        FROM Employee__c
        WHERE Accepts_Image__c = True
    """)

    # Process joint data
    def get_user_data(sf_user):
        return {
            "id": sf_user.get("Id"),
            "first_name": sf_user.get("Name"),
            "image_url": sf_user.get("Image_URL__c")
        }

    return {"data": {"response": list(map(get_user_data, sf_results)), "status": 200}}
