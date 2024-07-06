from functools import wraps
from firebase_functions import https_fn
from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from firebase_functions import logger

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def admin_get_week_codes(data):
    """HTTPS Cloud Function to get week codes."""
    # Initialize the Salesforce client
    sf, message, success = getSF()
    if not success:
        return {"data": {"error": message, "status": 401}}

    # Get the week codes from Salesforce
    week_codes = list(map(lambda x: {"code": x["code"], "name": x["period"]}, sf.get_camp_weeks()))

    # Return the response
    return {"data": {"response": week_codes, "status": 200}}
