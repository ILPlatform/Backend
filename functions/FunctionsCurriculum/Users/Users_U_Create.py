from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth, firestore
from Salesforce import getSF
from Emails import send_email_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=0)
def users_u_create(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters
    details = data.get("details")
    if not details:
        return {"data": {"response": "User details are required", "status": 400}}

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

    # Send an email to admins to notify them of the new user
    send_email_admin("New Teacher Registration", f"""
        <p>Dear Admin,</p>
        <p>A new teacher has registered on the platform. Please review the details below:</p>
        <ul>
            <li><b>Name:</b> {create_data.get("Name")} {create_data.get("Last_Name__c")}</li>
            <li><b>Email:</b> {create_data.get("Email__c")}</li>
            <li><b>Phone:</b> {create_data.get("Phone__c")}</li>
            <li><b>Other Phone:</b> {create_data.get("Other_Phone__c")}</li>
            <li><b>Nationality:</b> {create_data.get("Nationality__c")}</li>
            <li><b>Birthplace:</b> {create_data.get("Birthplace__c")}</li>
            <li><b>Registration Number:</b> {create_data.get("Registration_Number__c")}</li>
            <li><b>T-Shirt Size:</b> {create_data.get("T_Shirt_Size__c")}</li>
            <li><b>IBAN:</b> {create_data.get("IBAN__c")}</li>
            <li><b>BIC:</b> {create_data.get("BIC__c")}</li>
            <li><b>Address:</b> {create_data.get("Address__Street__s")}, {create_data.get("Address__PostalCode__s")} {create_data.get("Address__City__s")}</li>
            <li><b>Accepts Image:</b> {create_data.get("Accepts_Image__c")}</li>
            <li><b>Image URL:</b> {create_data.get("Image_URL__c")}</li>
        </ul>
        <p>Best regards,<br></p>
        """)

    return {"data": {"response": "User created successfully", "status": 200}}
