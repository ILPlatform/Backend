from Salesforce import getSF
from firebase_functions import logger, https_fn
from Actions.CampsForm import get_camps_form
from Google import GoogleConnector, ConventionDocument
from Helpers import firebase_functions_custom, https_fn_custom
from Emails import send_convention

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
    convention = ConventionDocument(google, teacher_details)
    convention.fill()
    link = convention.get_download_link()

    # Get link and send convention
    teacher_details.update({"link": link})
    send_convention(teacher_details)

    return {"data": {"response": link, "status": 200}}
