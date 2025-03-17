from Salesforce import getSF
from firebase_functions import logger, https_fn
from Actions.CampsForm import get_camps_form
from Google import GoogleConnector
from Helpers import firebase_functions_custom, https_fn_custom
from Emails import send_convention

from datetime import date

@https_fn_custom()
@firebase_functions_custom(auth_level=0)
def admin_update_teacher_contract_signed(data):
    """HTTPS Cloud Function to create convention."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Update contract record on Salesforce
    sf.update_contract(data.get("SF_Code"), data.get("Google_Link"))

    return {"data": {"response": "Success", "status": 200}}
