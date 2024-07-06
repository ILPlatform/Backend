from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from firebase_functions import logger, https_fn, options

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def admin_get_teachers_partners(data):
    """HTTPS Cloud Function to get teacher details for partners."""
    # Initialize the Salesforce client
    sf, message, success = getSF()
    if not success:
        return {"data": {"error": sf, "status": 401}}

    # Grab the parameters
    partner = data["partner"]
    only_confirmed = data["only_confirmed"]
    if partner is None:
        return {"data": {"error": "No text parameter provided", "status": 400}}

    # Log the request
    logger.log(f"[LOG] Getting teachers for partner {partner} with only_confirmed {only_confirmed}")

    # Get the teachers from Salesforce
    teachers = sf.get_teachers_for_partners(partner, only_confirmed)

    # Return the response
    return {"data": {"response": teachers, "status": 200}}
