from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF
from Emails import send_email_user

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def users_a_reset_password(data):
    # Setup Salesforce
    sf = getSF()

    # Get the parameters
    user_id = data.get("user_id")

    # Give user claims
    if not user_id:
        return {"data": {"response": "User UID is required", "status": 400}}

    # Get the email of the user
    user = auth.get_user(user_id)
    user_email = user.email

    # Get the user's name
    user_name = sf.sf.query(f"SELECT Name FROM Employee__c WHERE Firebase_UID__c = '{user_id}'")["records"][0].get("Name")

    # Generate password reset link
    reset_link = auth.generate_password_reset_link(user_email)

    # Send email to the user
    send_email_user(user_email, "Reset your Password for ILPlatform",
        f"""
        <p>Hello {user_name},</p>
        <p>Your password has been successfully reset. To continue, please follow the steps below:</p>
        <ol>
            <li><strong>Change your password:</strong> Click on the following link to set a new password: <a href="{reset_link}">Change my password</a>.</li>
            <li><strong>Log in to the platform:</strong> After changing your password, you can log in to the ILPlatform curriculum website using the <a href="https://curriculum.ilplatform.be">following link</a>.</li>
        </ol>
        <p>Remember, the curriculum website is your central hub for all information related to your classes, personal documents, and administrative procedures. We encourage you to log in as soon as possible to ensure you have access to all the resources you need.</p>
        <p>Thank you and best regards,</p>
        """)

    return {
        "data": {
            "response": "Success",
            "status": 200
        }
    }
