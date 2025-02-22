from Helpers import firebase_functions_custom, https_fn_custom, safe_create
from Salesforce import getSF
from Emails import send_email_user

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_create_custom(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters and check them
    details = data.get("details")
    if not (details and
            details.get("Teacher__c") and
            details.get("Unsigned_URL__c") and
            details.get("Description__c") and
            details.get("Teacher__r").get("Email__c")):
        return {"data": {"response": "Missing parameters", "status": 400}}

    # Create the document
    document = safe_create(sf.sf.Document__c, details | {"RecordTypeId": "012P5000001T9P7IAK"})

    # Send email to the user
    send_email_user(details.get("Teacher__r").get("Email__c"),
        "Nouveau Document Disponible",
        f"""
        <p>
            Bonjour {details.get("Teacher__r").get("Full_Name__c")},
        </p>
        <p>
            Un nouveau document ({details["Description__c"]}) est disponible pour toi. Tu peux le retrouver sur le <a href="https://curriculum.ilplatform.be">site curriculum</a>, sous "My Account" > "Documents", ou en pièce
            jointe à cet email.
        </p>
        <p>
            Merci de ne pas répondre à cet email. Si tu as des questions, merci de nous contacter via WhatsApp ou via <a href="mailto:daniel@ilplatform.be">daniel@ilplatform.be</a>.
        </p>
        <p>
            Merci et bien à toi,
        </p>
        """,
        file_url=details["Unsigned_URL__c"],
        file_name=details["Description__c"])

    return {"data": {"response": {"Id": document.get("id")}, "status": 200}}
