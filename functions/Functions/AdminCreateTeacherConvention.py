from Salesforce import getSF
from firebase_functions import logger, https_fn
from Actions.CampsForm import get_camps_form
from Google import GoogleConnector, ConventionDocument, ContractDocument
from Helpers import firebase_functions_custom, https_fn_custom
from Emails import send_convention

from datetime import date

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def admin_create_teacher_convention(data):
    """HTTPS Cloud Function to create convention."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Check if the week_codes are provided
    if data["email"] is None:
        return {"data": {"error": "No email provided", "status": 400}}

    # Get teacher details
    teacher_details = sf.get_teacher_details(data["email"])

    # Create and fill convention
    if data.get("contract") == "true":
        if not data.get("end_date"):
            raise ValueError("No end_date provided for contract")
        document = ContractDocument(google, teacher_details, end_date=data["end_date"])
    else:
        document = ConventionDocument(google, teacher_details)
    document.fill()
    link = document.get_download_link()

    # Create contract record on Salesforce
    sf_id = sf.create_contract(teacher_details.get("id"), str(date.today()), data.get("end_date") or "2024-08-31", "Student Contract" if data.get("contract") == "true" else "Convention", link)

    # Get link and send convention
    teacher_details.update({"link": link})
    teacher_details.update({"sf_id": sf_id})

    print(teacher_details)

    send_convention(teacher_details)

    return {"data": {"response": link, "status": 200}}
