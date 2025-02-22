from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import firestore
from Salesforce import getSF
from Emails import send_email_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def users_u_update(data):
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

    # Retrieve old data
    old_data = sf.sf.Employee__c.get(user_id)
    print(old_data)

    # Update the user in Salesforce
    sf.sf.Employee__c.update(user_id, update_data)

    # Send an email to admins to notify them of the new user
    send_email_admin("Teacher Update", f"""
        <p>Dear Admin,</p>
        <p>A new teacher has registered on the platform. Please review the details below:</p>
        <ul>
            <li><b>Name:</b>
                {old_data.get("Name")} {old_data.get("Last_Name__c")}
                -> {update_data.get("Name")} {update_data.get("Last_Name__c")}
            </li>
            <li><b>Email:</b> {old_data.get("Email__c")} -> {update_data.get("Email__c")}</li>
            <li><b>Phone:</b> {old_data.get("Phone__c")} -> {update_data.get("Phone__c")}</li>
            <li><b>Other Phone:</b>
                {old_data.get("Other_Phone__c")} -> {update_data.get("Other_Phone__c")}
            </li>
            <li><b>Nationality:</b> {old_data.get("Nationality__c")} -> {update_data.get("Nationality__c")}</li>
            <li><b>Birthplace:</b> {old_data.get("Birthplace__c")} -> {update_data.get("Birthplace__c")}</li>
            <li><b>Registration Number:</b> {old_data.get("Registration_Number__c")} -> {update_data.get("Registration_Number__c")}</li>
            <li><b>T-Shirt Size:</b> {old_data.get("T_Shirt_Size__c")} -> {update_data.get("T_Shirt_Size__c")}</li>
            <li><b>IBAN:</b> {old_data.get("IBAN__c")} -> {update_data.get("IBAN__c")}</li>
            <li><b>BIC:</b> {old_data.get("BIC__c")} -> {update_data.get("BIC__c")}</li>
            <li><b>Address:</b>
                {old_data.get("Address__Street__s")}, {old_data.get("Address__PostalCode__s")} {old_data.get("Address__City__s")}
                ->
                {update_data.get("Address__Street__s")}, {update_data.get("Address__PostalCode__s")} {update_data.get("Address__City__s")}
            </li>
            <li><b>Accepts Image:</b> {old_data.get("Accepts_Image__c")} -> {update_data.get("Accepts_Image__c")}</li>
            <li><b>Image URL:</b> {old_data.get("Image_URL__c")} -> {update_data.get("Image_URL__c")}</li>
        </ul>
        <p>Best regards,<br></p>
        """)

    return {"data": {"response": "User updated successfully", "status": 200}}
