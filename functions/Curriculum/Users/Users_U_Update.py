from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def users_U_update(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    uid = data.get("uid")
    details = data.get("details")

    if not uid or not details:
        return {"data": {"response": "User UID and details are required", "status": 400}}

    # Retrieve the user by UID
    user_id = sf.sf.query(f"""
        SELECT Id
        FROM Employee__c
        WHERE Firebase_UID__c='{uid}'
    """).get("records", [{}])[0].get("Id")

    if not user_id:
        return {"data": {"response": "User not found", "status": 400}}

    # Prepare the update data
    update_data = {
        "Name": details.get("first_name"),
        "Last_Name__c": details.get("last_name"),
        "Phone__c": details.get("phone"),
        "Other_Phone__c": details.get("other_phone"),
        "Nationality__c": details.get("nationality"),
        "Birthplace__c": details.get("birthplace"),
        "Registration_Number__c": details.get("registration_number"),
        "T_Shirt_Size__c": details.get("t_shirt_size"),
        "IBAN__c": details.get("iban"),
        "BIC__c": details.get("bic"),
        "Address__Street__s": details.get("address_street"),
        "Address__City__s": details.get("address_city"),
        "Address__PostalCode__s": details.get("address_zip"),
    }

    # Ensure no field is empty, expect possibly Other_Phone__c and T_Shirt_Size__c
    for key, value in update_data.items():
        if not value and key not in ["Other_Phone__c", "T_Shirt_Size__c"]:
            return {"data": {"response": f"Field '{key}' is required", "status": 400}}

    if not update_data:
        return {"data": {"response": "No valid fields to update", "status": 400}}

    # Update the user in Salesforce
    sf.sf.Employee__c.update(user_id, update_data)
    return {"data": {"response": "User updated successfully", "status": 200}}
