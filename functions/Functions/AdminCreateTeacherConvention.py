from Salesforce import getSF
from firebase_functions import logger, https_fn
from Actions.CampsForm import get_camps_form
from Google import GoogleConnector, ContractDocument
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
        raise ValueError("No email provided for contract")
    if not data.get("end_date"):
        raise ValueError("No end_date provided for contract")

    # Get teacher details
    teacher_details = sf.get_teacher_details(data["email"])

    # Get contract type
    type = data.get("contract")

    # Create and fill convention
    document = ContractDocument(google, teacher_details, data["end_date"], type)
    document.fill()
    link = document.get_download_link()

    # Create contract record on Salesforce
    sf_id = sf.create_contract(teacher_details.get("id"), str(date.today()), data.get("end_date") or "2024-08-31", type, link)

    # Get link and send convention
    teacher_details.update({"link": link})
    teacher_details.update({"sf_id": sf_id})

    print(teacher_details)

    send_convention(teacher_details)

    return {"data": {"response": link, "status": 200}}
