from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import firestore, auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def users_a_update_roles(data):
    # Get the parameters
    user_uid = data.get("user_uid")
    roles = data.get("roles")
    if not user_uid:
        return {"data": {"response": "User UID is required", "status": 400}}
    # if "super_admin" in roles:
    #     return {"data": {"response": "Cannot assign super admin role", "status": 400}}

    # Give user claims
    user = auth.get_user(user_uid)
    auth.set_custom_user_claims(user_uid, user.custom_claims | {"roles": roles})

    return {"data": {"response": "Success", "status": 200}}
