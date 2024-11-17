from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF
from Actions import update_and_create_classes_per_week
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime

# from Emails.SendEmailReplacementsOneTime import send_email_replacement_onetime, send_email_replacement_onetime_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def additional_a_get_all(data):
    # Initialize the Salesforce client
    sf = getSF()

    # Get all the one-time replacements
    results = sf.sf.query_all_iter(f"""
        SELECT
            Id, CreatedDate, Date__c, RecordTypeId,
            Teacher__r.Name, Teacher__r.Last_Name__c, Teacher__r.Id,
            Opportunity__r.Code__c, Opportunity__r.Start_Time__c, Opportunity__r.End_Time__c, Opportunity__r.Account.Name, Opportunity__r.Day_of_Week__c, Opportunity__r.Id
        FROM Replacement__c
        WHERE Opportunity__r.RecordTypeId = '012060000003OPWAA2'
            AND (RecordTypeId = '012P5000001YwypIAC')
            AND Deleted__c = False
    """)

    # Format the one-time replacements
    replacements = [{
        "id": result.get("Id"),
        "code": result.get("Opportunity__r").get("Code__c"),
        "class_id": result.get("Opportunity__r").get("Id"),
        "school": result.get("Opportunity__r").get("Account").get("Name"),
        "created_timestamp": result.get("CreatedDate"),
        "date": result.get("Date__c"),
        "day": result.get("Opportunity__r").get("Day_of_Week__c"),
        "time": f"{result.get('Opportunity__r').get('Start_Time__c')[:5]}-{result.get('Opportunity__r').get('End_Time__c')[:5]}",
        "teacher": f"{result.get('Teacher__r').get('Name')} {result.get('Teacher__r').get('Last_Name__c')}" if result.get('Teacher__r') else None,
        "teacher_id": result.get("Teacher__r").get("Id") if result.get("Teacher__r") else None,
    } for result in results]

    return {"data": {"response": replacements, "status": 200}}
