from Salesforce import getSF
from firebase_functions import logger, https_fn
from Google import GoogleConnector, TimesheetDocument
from Helpers import firebase_functions_custom, https_fn_custom
from Emails import send_convention
from Google import Events
from pprint import pprint
from Actions import generate_confirmation_text, get_teacher_dict, update_payment_sheet
from Emails import send_attestation_teacher, send_attestation_admin
from firebase_admin import firestore, auth

BLACKLIST_EMAILS = [
  # '.*@ilplatform.be',
  'luca.paraschi@gmail.com',
  'mihneataranu@gmail.com',
  'alexandra-demt@hotmail.com',
  'chris.kafrouni@gmail.com'
]

@https_fn_custom(timeout_sec=540)
@firebase_functions_custom(auth_level=2)
def attestations_a_create(data):
    """HTTPS Cloud Function to create monthly attestations. This version runs once the proposal has been confirmed."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Check if the week_codes are provided
    try:
        year = int(data["year"])
        month = int(data["month"])
    except Exception as e:
        raise ValueError(f"Year or month not provided or not an integer -> {e}")

    # Get events
    events = Events(google, year, month, BLACKLIST_EMAILS).get_events(sf)

    # Get teacher details
    teacher_dict = get_teacher_dict(sf, events)

    # Filter the teacher_dict if a name is provided
    if data.get("teacher_id"):
        try:
            named_teacher = list(filter(lambda x: teacher_dict.get(x).get("id").lower().replace(" ", "") == data["teacher_id"].lower().replace(" ", ""), teacher_dict))
            assert len(named_teacher) == 1
            teacher_dict = {named_teacher[0]: teacher_dict.get(named_teacher[0])}
        except Exception as e:
            raise ValueError(f"Teacher {data['teacher_id']} not found in the events -> {e}.")

    # Generate the confirmation text if confirmation is required
    return_string = generate_confirmation_text(teacher_dict, events)
    if data.get("require_confirm"):
        return {"data": {"response": return_string, "status": 200}}

    # Update the payment sheet
    update_payment_sheet(google, teacher_dict, year, month)

    # Create the timesheets, send the emails and add the document to Firestore
    for teacher_email in teacher_dict:
        teacher = teacher_dict.get(teacher_email)
        Timesheet = TimesheetDocument(google, teacher, year, month)
        Timesheet.fill()

        teacher.update({"link": Timesheet.get_download_link()})
        send_attestation_teacher(teacher, year, month, True if len(teacher_dict) == 1 else False)

        # Add the document to Salesforce
        sf.sf.Document__c.create({
            "Year__c": year,
            "Month__c": month,
            "Teacher__c": teacher.get("id"),
            "Type__c": "Attestation",
            "Description__c": f"Attestation - {year}/{month}",
            "Unsigned_URL__c": teacher.get("link"),
            "RecordTypeId": "012P5000001T8MbIAK",
            "To_Sign__c": True,
        })

    # Send the confirmation email to the admin
    send_attestation_admin(return_string, year, month)

    return {"data": {"response": "Success", "status": 200}}

def get_user_uid_by_email(email):
    try:
        # Get user by email
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception as e:
        raise ValueError(f"Error fetching user data: {e}")
        return None
