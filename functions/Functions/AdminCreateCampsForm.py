from Salesforce import getSF
from firebase_functions import logger, https_fn
import json
from Actions.CampsForm import get_camps_form
from Google.Connector import GoogleConnector
from Helpers import firebase_functions_custom, https_fn_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def admin_create_camps_form(data):
    """HTTPS Cloud Function to create camps form."""
    # Initialize the Salesforce client
    sf, message, success = getSF()
    if not success:
        return {"data": {"error": message, "status": 401}}

    # Initialize the Google client
    google = GoogleConnector()

    # Check if the week_codes are provided
    if data["week_codes"] is None:
        return {"data": {"error": "No week_codes or title provided", "status": 400}}

    # Create camps form
    message, success = get_camps_form(google, sf, data["title"], data["week_codes"])
    if not success:
        return {"data": {"error": message, "status": 400}}
    return {"data": {"response": message, "status": 200}}
