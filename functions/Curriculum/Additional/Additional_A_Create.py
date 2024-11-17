from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime

# from Emails.SendEmailReplacementsOneTime import send_email_replacement_onetime, send_email_replacement_onetime_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def additional_a_create(data):
    # Initialize the Salesforce client
    sf = getSF()

    # Create a new additional teacher object on SF
    sf.sf.Replacement__c.create({
        "RecordTypeId": "012P5000001YwypIAC",
        "Teacher__c": data["teacher_id"],
        "Date__c": data["date"],
        "Opportunity__c": data["class_id"]
    })

    return {"data": {"response": "Success", "status": 200}}
