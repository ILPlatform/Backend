from Salesforce import getSF
from firebase_functions import logger, https_fn
from Actions.CampsForm import get_camps_form
from Google import GoogleConnector, ContractDocument
from Helpers import firebase_functions_custom, https_fn_custom
from Emails import send_email_user
from datetime import date

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def docs_a_create_contract(data):
    """HTTPS Cloud Function to create convention."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Get parameters
    teacher_id = data.get("teacher_id")
    end_date = data.get("end_date")
    type = data.get("type")

    # Check if the week_codes are provided
    if teacher_id is None:
        raise ValueError("No email provided for contract")
    if not end_date:
        raise ValueError("No end_date provided for contract")

    # Get teacher email
    teacher_email = sf.sf.query(f"""
        SELECT Email__c
        FROM Employee__c
        WHERE Id='{teacher_id}'
    """).get("records")[0].get("Email__c")

    # Get teacher details
    teacher_details = sf.get_teacher_details(teacher_email)

    # Create and fill convention
    document = ContractDocument(google, teacher_details, end_date, type)
    document.fill()
    link = document.get_download_link()

    # Create contract record on Salesforce
    document = sf.sf.Document__c.create({
        "Description__c": type,
        "Teacher__c": teacher_details.get("id"),
        "Type__c": type,
        "To_Sign__c": True,
        "Unsigned_URL__c": link,
        "RecordTypeId": "012P5000001T9QjIAK"
    })

    # Send email to the user
    send_email_user(teacher_details.get("email"), "New Document Available", f"""
        <p>
            Bonjour,
        </p>
        <p>
            Un nouveau document ({type}) est disponible pour toi. Tu peux le retrouver sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents".
        </p>
        <p>
            Merci de ne pas répondre à cet email. Si tu as des questions, merci de nous contacter via WhatsApp ou via <a href="mailto:daniel@ilplatform.be">daniel@ilplatform.be</a>.
        </p>
        <p>
            Merci et bien à toi,
        </p>
        """)

    return {"data": {"response": {
        "Id": document.get("id"),
        "Unsigned_URL__c": link,
    }, "status": 200}}
