from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth, firestore
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def users_U_create(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters
    uid = data.get("uid")
    details = data.get("details")
    if not uid or not details:
        return {"data": {"response": "User UID and details are required", "status": 400}}

    # Check user provided consent
    if not details.get("consent"):
        return {"data": {"response": "User must provide consent", "status": 400}}

    # Check email is not already in use on SF
    result = sf.sf.query(f"SELECT Id FROM Employee__c WHERE Email__c='{details.get('email')}'")
    if len(result.get("records")) > 0:
        return {"data": {"response": "Email already in use on SF", "status": 400}}

    # Check email is not already in use on Firebase Auth
    try:
        user = auth.get_user_by_email(details.get("email"))
        if user:
            return {"data": {"response": "Email already in use on Firebase", "status": 400}}
    except:
        pass

    # Prepare the update data
    create_data = {
        "Name": details.get("first_name"),
        "Last_Name__c": details.get("last_name"),
        "Email__c": details.get("email"),
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
        "Accepts_Image__c": details.get("accepts_image"),
        "Image_URL__c": details.get("image_url"),
    }

    # Ensure no field is empty, expect possibly Other_Phone__c and T_Shirt_Size__c
    for key, value in create_data.items():
        if not value and key not in ["Other_Phone__c", "T_Shirt_Size__c", "Accepts_Image__c"]:
            return {"data": {"response": f"Field '{key}' is required", "status": 400}}

    # Create the user in Salesforce
    sf.sf.Employee__c.create(create_data)
    return {"data": {"response": "User created successfully", "status": 200}}
