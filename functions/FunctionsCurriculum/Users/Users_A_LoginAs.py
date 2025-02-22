from Helpers import firebase_functions_custom, https_fn_custom
from firebase_admin import auth
from firebase_functions.params import IntParam, StringParam
import os

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def users_a_login_as(data):
    # Get the data
    details = data.get("details")
    if not details or not details.get("Firebase_UID__c"):
        return {"data": {"response": "Missing details", "status": 400}}

    try:
        # Generate a custom token for the user
        custom_token = auth.create_custom_token(details.get("Firebase_UID__c"))
        return {"data": {"response": {"token": custom_token.decode("utf-8")}, "status": 200}}
    except Exception as e:
        return {"data": {"response": e, "status": 400}}
