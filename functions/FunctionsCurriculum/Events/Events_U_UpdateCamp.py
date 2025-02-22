from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from Actions import update_and_create_camps
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options

@https_fn_custom(timeout_sec=540)
@firebase_functions_custom(auth_level=2)
def events_u_update_camp(data):
    """HTTPS Cloud Function to update calendar events for camps."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Update Calendar Events
    message, success = update_and_create_camps(google, sf, data["camp_id"])

    # # Create Picture Folders
    # create_camp_pictures(google, sf, data["week_codes"])

    return {"data": {"response": message, "status": 200}}
