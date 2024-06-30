# Firebase imports
from firebase_functions import firestore_fn, https_fn, options
from firebase_functions.core import init
from firebase_functions import logger
from firebase_admin import initialize_app, firestore
from firebase_functions.params import StringParam

# Custom imports
from Salesforce.SFProcessor import SFProcessor
from Google.Connector import GoogleConnector
from Actions.CampsEvents import update_and_create_camps_per_week
from Actions.CampsForm import get_camps_form

# Python imports
import os
import json



# Secret parameters
SF_USERNAME = StringParam("SF_USERNAME")
SF_PASSWORD = StringParam("SF_PASSWORD")
SF_SECURITY_TOKEN = StringParam("SF_SECURITY_TOKEN")

# Initialize the app
app = initialize_app()

# Initialize the Google client
google = GoogleConnector()

@https_fn.on_request()
def get_teachers_for_partners(req: https_fn.Request) -> https_fn.Response:
    """HTTPS Cloud Function to get teacher details for partners."""

    # Initialize the Salesforce client
    sf = SFProcessor(SF_USERNAME.value, SF_PASSWORD.value, SF_SECURITY_TOKEN.value)

    # Grab the parameters
    partner = req.args.get("partner")
    only_confirmed = req.args.get("only_confirmed") == "true"
    if partner is None:
        return https_fn.Response("No text parameter provided", status=400)

    # Log the request
    logger.log(f"[LOG] Getting teachers for partner {partner} with only_confirmed {only_confirmed}")

    # Get the teachers from Salesforce
    teachers = sf.get_teachers_for_partners(partner, only_confirmed)

    # Return the response
    return https_fn.Response("\n".join(teachers))

@https_fn.on_request(
    region='europe-west1',
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get", "post", "options"]
    ))
def get_week_codes(req: https_fn.Request) -> https_fn.Response:
    """HTTPS Cloud Function to get week codes."""

    # Initialize the Salesforce client
    sf = SFProcessor(SF_USERNAME.value, SF_PASSWORD.value, SF_SECURITY_TOKEN.value)

    # Log the request
    logger.log(f"[LOG] Getting week codes")

    # Get the week codes from Salesforce
    week_codes = list(map(lambda x: x["code"], sf.get_camp_weeks()))

    # Return the response
    return {"data": week_codes, "status": 200}

@https_fn.on_request()
def create_camps_for_a_week(req: https_fn.Request) -> https_fn.Response:
    """HTTPS Cloud Function to create camps for a week."""

    # Initialize the Salesforce client
    sf = SFProcessor(SF_USERNAME.value, SF_PASSWORD.value, SF_SECURITY_TOKEN.value)

    # Grab the parameters
    week_code = req.args.get("week_code")
    if week_code is None:
        return https_fn.Response("No text parameter provided", status=400)

    # Log the request
    logger.log(f"[LOG] Creating camps for week {week_code}")

    # Create camps for the week
    update_and_create_camps_per_week(google, sf, week_code)

    # Return the response
    return https_fn.Response("Camps created successfully")

@https_fn.on_request(
    region='europe-west1',
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get", "post", "options"]
    ))
def create_camps_form(req: https_fn.Request) -> https_fn.Response:
    """HTTPS Cloud Function to create camps form."""

    # Initialize the Salesforce client
    sf = SFProcessor(SF_USERNAME.value, SF_PASSWORD.value, SF_SECURITY_TOKEN.value)

    # Grab the parameters
    data = json.loads(req.data.decode('utf8').replace("'", '"'))["data"]
    title = data["title"]
    week_codes = data["week_codes"]
    if title is None or week_codes is None:
        return https_fn.Response("No text parameter provided", status=400)

    # Log the request
    logger.log(f"[LOG] Creating camps form with title {title} and week codes {week_codes}")

    # Create camps form
    link = get_camps_form(google, sf, title, week_codes.replace(" ", "").split(","))

    # Return the response
    return {"data": link, "status": 200}
