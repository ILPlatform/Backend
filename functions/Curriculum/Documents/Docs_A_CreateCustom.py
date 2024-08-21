# Function to create a new document in the database. Requires document admin level.

from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from Salesforce import getSF
from Emails import send_email_user

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_create_custom(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    teacher_id = data.get("teacher_id")
    url = data.get("url")
    to_sign = data.get("to_sign")
    type = data.get("type")
    year = data.get("year")
    month = data.get("month")

    if not teacher_id:
        return {"data": {"response": "Teacher ID is required", "status": 400}}
    if not url or not type or not year or not month:
        return {"data": {"response": "URL, to_sign, type, year and month are required", "status": 400}}

    # Get the user's name from SF
    result = sf.sf.query(f"SELECT Full_Name__c, Email__c, Id FROM Employee__c WHERE Id = '{teacher_id}'")
    if not result["records"]:
        return {"data": {"response": "User not found", "status": 400}}
    user_email = result.get("records")[0].get("Email__c")

    # Create the document
    sf.sf.Document__c.create({
        "Description__c": f"{type} {year}/{month}",
        "Teacher__c": teacher_id,
        "Type__c": type,
        "Year__c": year,
        "Month__c": month,
        "Unsigned_URL__c": url,
        "To_Sign__c": to_sign,
        "RecordTypeId": "012P5000001T9P7IAK"
    })

    # Send email to the user
    send_email_user(user_email, "New Document Available", f"""
        <p>
            Bonjour,
        </p>
        <p>
            Un nouveau document ({type} {year}/{month}) est disponible pour toi. Tu peux le retrouver sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents".
        </p>
        <p>
            Merci de ne pas répondre à cet email. Si tu as des questions, merci de nous contacter via WhatsApp ou via <a href="mailto:daniel@ilplatform.be">daniel@ilplatform.be</a>.
        </p>
        <p>
            Merci et bien à toi,
        </p>
        """)

    return {"data": {"response": "Success", "status": 200}}
