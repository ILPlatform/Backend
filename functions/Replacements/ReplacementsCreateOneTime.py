from Helpers import firebase_functions_custom, https_fn_custom
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from Salesforce import getSF

from Emails.SendEmailReplacementsOneTime import send_email_replacement_onetime, send_email_replacement_onetime_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def replacements_create_one_time(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the parameters
    class_code = data.get("class_code")
    date = data.get("date")
    user_email = data.get("user_email")
    reason = data.get("reason")
    if not class_code or not date:
        return {"data": {"response": "Class code and date are required", "status": 400}}, 400

    # Get the class details
    class_details = sf.get_all_class_details2(class_code)

    # Ensure the class exists
    if not class_details:
        return {"data": {"response": f"Class with code {class_code} does not exist", "status": 400}}

    # Ensure the indicated date coincides with a class date
    if not datetime.strptime(date, "%Y-%m-%d").strftime("%A") == class_details.get("event", {}).get("day"):
        return {"data": {"response": f"The indicated date does not coincide with the class day of {class_details.get('event', {}).get('day')}", "status": 400}}

    # Get the Opportunity ID
    opportunity_id = class_details.get("id")

    # Retrieve the Employee ID from email
    try:
        employee_id = sf.sf.query(f"SELECT Id FROM Employee__c WHERE Email__c = '{user_email}'").get("records", [{}])[0].get("Id")
    except Exception as e:
        return {"data": {"response": f"Employee with email {user_email} does not exist", "status": 400}}

    # Create a new one time replacement on the given date
    sf.sf.Replacement__c.create({
        "Teacher_Old__c": employee_id,
        "Opportunity__c": opportunity_id,
        "Date__c": date,
        "RecordTypeId": "012P5000001QASzIAO",
        "Reason__c": reason
    })

    # Send email to the teacher
    send_email_replacement_onetime(user_email, f"{class_code} - {class_details['event']['school']} ({class_details['event']['start_time'][:5]}-{class_details['event']['end_time'][:5]})", date)

    # Send email to admins
    send_email_replacement_onetime_admin(user_email, f"{class_code} - {class_details['event']['school']} ({class_details['event']['start_time'][:5]}-{class_details['event']['end_time'][:5]})", date)

    # Initialize the Google client
    google = GoogleConnector()

    return {"data": {"response": "Replacement recorded successfully.", "status": 200}}
