# Function to get all documents related to an authenticated user. Requires authentication.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import firestore, auth
from Salesforce import getSF
from Emails import send_email_user

@https_fn_custom(access=True)
@firebase_functions_custom(auth_level=0)
def customers_e_create(data):
    # Initialize DB and SF
    # sf = getSF()

    # Get the parameters
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    phone = data.get("phone")
    consent = data.get("consent")

    print(data)

    if not first_name or not last_name or not email or not phone or not consent:
        return {"data": {"response": "Missing parameters", "status": 400}}

    # Send email to Thoothe
    send_email_user("thoothe@ilplatform.be", "New Customer Registered", f"""
        <p>Hello Thoothe,</p>
        <p>A new customer has registered on the platform:</p>
        <ul>
            <li><strong>First Name:</strong> {first_name}</li>
            <li><strong>Last Name:</strong> {last_name}</li>
            <li><strong>Email:</strong> {email}</li>
            <li><strong>Phone:</strong> {phone}</li>
            <li><strong>Consent:</strong> {consent}</li>
        </ul>
        <p>Thank you and best regards,</p>
    """)

    return {"data": {"response": "Success", "status": 200}}
