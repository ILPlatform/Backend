from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from Actions.CampsEvents import update_and_create_camps_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def admin_update_camps_events(data):
    """HTTPS Cloud Function to update calendar events for camps."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Log the request
    message, success = update_and_create_camps_per_week(google, sf, data["week_codes"])
    return {"data": {"response": message, "status": 200}}
