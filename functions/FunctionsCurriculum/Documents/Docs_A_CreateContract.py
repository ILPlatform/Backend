from Salesforce import getSF
from Google import GoogleConnector, ContractDocument
from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Emails import send_email_user

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def docs_a_create_contract(data):
    """HTTPS Cloud Function to create convention."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Get parameters
    details = data.get("details")
    if not (details and
        details.get("Type__c") and
        details.get("End_Date__c") and
        details.get("Teacher__c")):
        return {"data": {"response": "Missing parameters", "status": 400}}

    # Get teacher email
    teacher_email = sf.sf.query(f"""
        SELECT Email__c
        FROM Employee__c
        WHERE Id='{details["Teacher__c"]}'
    """).get("records")[0].get("Email__c")

    # Get teacher details
    teacher_details = sf.get_teacher_details(teacher_email)

    # Create and fill convention
    document = ContractDocument(google, teacher_details, details["End_Date__c"], details["Type__c"])
    document.fill()
    link = document.get_download_link()

    # Add RecordTypeId
    details.update({
        "RecordTypeId": "012P5000001T9QjIAK",
        "Unsigned_URL__c": link,
        "To_Sign__c": True
    })

    # Create contract record on Salesforce
    document = safe_create(sf.sf.Document__c, details)

    # Send email to the user
    send_email_user(teacher_details.get("email"), "New Document Available", f"""
        <p>
            Bonjour,
        </p>
        <p>
            Un nouveau document ({details["Type__c"]}) est disponible pour toi. Tu peux le retrouver sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents".
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
