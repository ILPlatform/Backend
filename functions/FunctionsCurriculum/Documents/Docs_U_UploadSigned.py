from Helpers import firebase_functions_custom, https_fn_custom
from datetime import datetime
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def docs_u_upload_signed(data):
    # Initialize SF
    sf = getSF()

    # Get the parameters
    details = data.get("details")
    if not details or not details.get("Id"):
        return {"data": {"response": "Document ID is required", "status": 400}}

    # Retrieve the document
    document = sf.sf.Document__c.get(details.get("Id"))
    if not document:
        return {"data": {"response": "Document not found", "status": 404}}

    if document.get("To_Sign__c") and not details.get("Signed_URL__c"):
        return {"data": {"response": "Signed URL is required when signature is required", "status": 400}}

    # Update the document
    sf.sf.Document__c.update(document.get("Id"), {
        "Signed__c": True,
        "Signed_URL__c": details.get("Signed_URL__c"),
        "Signed_Timestamp__c": datetime.now().strftime("%Y-%m-%d"+"T"+"%H:%M:%S"+"Z")
    })

    return {"data": {"response": "Successfully Signed Contract", "status": 200}}
