# from google.cloud.firestore_v1.base_query import FieldFilter
# from Helpers import firebase_functions_custom, https_fn_custom
# from Google.Connector import GoogleConnector
# from firebase_functions import https_fn, options
# from datetime import datetime
# from Salesforce import getSF

# @https_fn_custom()
# @firebase_functions_custom(auth_level=1)
# def curriculum_get_user(data):
#     # Initialize DB and SF
#     sf = getSF()

#     # Get the parameters
#     uid = data.get("uid")
#     user_email = data.get("user_email")

#     # Give user claims
#     if not uid and not user_email:
#         return {"data": {"response": "User UID or email is required", "status": 400}}

#     # Get the user
#     result = sf.sf.query(f"SELECT Id FROM Employee__c WHERE Email__c='{user_email}'")
#     if len(result.get("records")) == 0:
#         return {"data": {"response": "User not found", "status": 400}}

#     # Get all contracts of the given user
#     contracts = db.collection("Documents").where(filter=FieldFilter("uid", "==", uid)).where(filter=FieldFilter("signed", "==", False)).stream()

#     # Compute number of unsigned contracts
#     unsigned_contracts = 0
#     for contract in contracts:
#         if not contract.to_dict().get("deleted"):
#             unsigned_contracts += 1

#     return {"data": {"response": {"nb_documents": unsigned_contracts}, "status": 200}}
