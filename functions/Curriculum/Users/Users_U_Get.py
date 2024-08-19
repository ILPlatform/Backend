from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def users_U_get(data):
    # Initialize DB and SF
    db = firestore.client()
    sf = getSF()

    # Get the parameters
    uid = data.get("uid")

    # Give user claims
    if not uid and not user_email:
        return {"data": {"response": "User UID or email is required", "status": 400}}

    # Get the user
    result = sf.sf.query(f"""
        SELECT
            Id,
            Name, Last_Name__c, Email__c, Phone__c, Other_Phone__c,
            Nationality__c, Birthplace__c, Registration_Number__c,
            T_Shirt_Size__c,
            IBAN__c, BIC__c,
            Address__Street__s, Address__City__s, Address__PostalCode__s
        FROM Employee__c
        WHERE Firebase_UID__c='{uid}'
    """).get("records", [{}])[0]
    if not result.get("Id"):
        return {"data": {"response": "User not found", "status": 400}}

    # Process the user data
    user = {
        "id": result.get("Id"),
        "first_name": result.get("Name"),
        "last_name": result.get("Last_Name__c"),
        "email": result.get("Email__c"),
        "phone": result.get("Phone__c"),
        "other_phone": result.get("Other_Phone__c"),
        "nationality": result.get("Nationality__c"),
        "birthplace": result.get("Birthplace__c"),
        "registration_number": result.get("Registration_Number__c"),
        "t_shirt_size": result.get("T_Shirt_Size__c"),
        "iban": result.get("IBAN__c"),
        "bic": result.get("BIC__c"),
        "address_street": result.get("Address__Street__s"),
        "address_city": result.get("Address__City__s"),
        "address_zip": result.get("Address__PostalCode__s"),
    }

    # Get all contracts of the given user
    contracts = db.collection("Documents").where(filter=FieldFilter("uid", "==", uid)).where(filter=FieldFilter("signed", "==", False)).stream()

    # Flag if the user has entries that are none that are not other_phone or t_shirt_size
    settings_require_update = False
    print(user.get("birthplace"))
    for key, value in user.items():
        if value is None and key not in ["other_phone", "t_shirt_size"]:
            settings_require_update = True


    # Compute number of unsigned contracts
    unsigned_contracts = 0
    for contract in contracts:
        if not contract.to_dict().get("deleted"):
            unsigned_contracts += 1

    return {
        "data": {
            "response": {
                "nb_documents": unsigned_contracts,
                "settings_require_update": settings_require_update,
                "details": user
            },
            "status": 200
        }
    }
