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
def users_a_create(data):
    # Get the Salesforce connector
    sf = getSF()

    # Get the parameters
    if not data.get("Id"):
        return {"data": {"response": "User ID is required", "status": 400}}

    # Retrieve user email
    user = sf.sf.query(f"""
        SELECT Email__c, Name
        FROM Employee__c
        WHERE Id = '{data["Id"]}'
    """)["records"][0]
    user_email = user.get("Email__c")
    user_name = user.get("Name")

    # Create Firebase Auth account
    user = auth.create_user(email=user_email)

    # Save the user UID to the Salesforce record
    sf.sf.Employee__c.update(user_id, {"Firebase_UID__c": user.uid})

    # Generate password reset link
    reset_link = auth.generate_password_reset_link(user_email)

    # Send email to the user
    send_email_user(user_email, "Account Created for ILPlatform",
        f"""
        <p>Hello {user_name},</p>

        <p>We are pleased to inform you that an account has been created for you on the ILPlatform curriculum website. This platform is your central hub for all things related to your classes, including:</p>

        <ul>
            <li>Details about the classes you will be teaching.</li>
            <li>All your personal documents.</li>
            <li>Administrative procedures.</li>
        </ul>

        <p>Your account has been created using the email address: <strong>{user_email}</strong>.</p>

        <p>To get started, please follow the steps below:</p>

        <ol>
            <li><strong>Set your password:</strong> Click on the following link to set your password: <a href="{reset_link}">Set my password</a>.</li>
            <li><strong>Log in to the platform:</strong> Once your password is set, you can log in to the ILPlatform curriculum website by visiting the <a href="https://curriculum.ilplatform.be">following link</a>.</li>
        </ol>

        <p>This website is an important tool to use during your time at ILPlatform. We recommend that you log in as soon as possible to familiarize yourself with the platform.</p>

        <p>Thank you and we look forward to your active participation!</p>

        <p>Best regards,</p>

        <p>The ILPlatform Team</p>
        """)

    return {
        "data": {
            "response": "Success",
            "status": 200
        }
    }
