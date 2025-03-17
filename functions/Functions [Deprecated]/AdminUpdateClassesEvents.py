from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options

@https_fn_custom(timeout_sec=540)
@firebase_functions_custom(auth_level=2)
def admin_update_classes_events(data):
    """HTTPS Cloud Function to update calendar events for camps."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Update Calendar Events
    message, success = update_and_create_classes_per_week(google, sf, year_code=data["year_code"])

    return {"data": {"response": message, "status": 200}}
