from Salesforce import getSF
from firebase_functions import logger, https_fn
from Google import GoogleConnector, TimesheetDocument
from Helpers import firebase_functions_custom, https_fn_custom
from Emails import send_convention
from Google import Events
from pprint import pprint
from Actions import generate_confirmation_text, get_teacher_dict, update_payment_sheet
from Emails import send_attestation_teacher, send_attestation_admin

BLACKLIST_EMAILS = [
  '.*@ilplatform.be',
  'luca.paraschi@gmail.com',
  'mihneataranu@gmail.com',
  'alexandra-demt@hotmail.com',
  'chris.kafrouni@gmail.com'
]

@https_fn_custom(timeout_sec=540)
@firebase_functions_custom(auth_level=2)
def admin_create_teacher_attestations(data):
    """HTTPS Cloud Function to create monthly attestations. This version runs once the proposal has been confirmed."""
    # Initialize the Salesforce client
    sf = getSF()

    # Initialize the Google client
    google = GoogleConnector()

    # Check if the week_codes are provided
    year = data["year"]
    month = data["month"]
    if year is None or month is None:
        raise ValueError("No year or month provided")

    # Get events
    events = Events(google, year, month, BLACKLIST_EMAILS).get_events(sf)

    # Get teacher details
    teacher_dict = get_teacher_dict(sf, events)

    # Filter the teacher_dict if a name is provided
    if data["name"]:
        try:
            named_teacher = list(filter(lambda x: teacher_dict.get(x).get("name").lower().replace(" ", "") == data["name"].lower().replace(" ", ""), teacher_dict))
            assert len(named_teacher) == 1
            teacher_dict = {named_teacher[0]: teacher_dict.get(named_teacher[0])}
        except Exception as e:
            raise ValueError(f"Teacher {data['name']} not found in the events -> {e}.")

    # Generate the confirmation text if confirmation is required
    return_string = generate_confirmation_text(teacher_dict, events)
    if data.get("require_confirm"):
        return {"data": {"response": return_string, "status": 200}}

    # Update the payment sheet
    update_payment_sheet(google, teacher_dict, year, month)

    # Create the timesheets and send the emails
    for teacher_email in teacher_dict:
        teacher = teacher_dict.get(teacher_email)
        Timesheet = TimesheetDocument(google, teacher, year, month)
        Timesheet.fill()

        teacher.update({"link": Timesheet.get_download_link()})
        send_attestation_teacher(teacher, year, month, True if len(teacher_dict) == 1 else False)

    # Send the confirmation email to the admin
    send_attestation_admin(return_string, year, month)

    return {"data": {"response": "Success", "status": 200}}
