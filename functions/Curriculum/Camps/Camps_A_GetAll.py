from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def camps_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the user
    result = sf.sf.query_all_iter(f"""
        SELECT
            Id, Code__c, Account.Name,
            Week__r.Start_Date__c, Week__r.End_Date__c, Week__r.Name,
            Time_Schedule__r.Name, Ages_Real__c, StageName,
            Teacher__r.Id, Teacher__r.Full_Name__c, Teacher__r.Firebase_UID__c,
            Google_Event__c
        FROM Opportunity
        WHERE RecordTypeId = '012060000003OPRAA2'
    """)

    # Process the result
    codes = [{
        "id": code.get("Id"),
        "code": code.get("Code__c"),
        "time": code.get("Time_Schedule__r").get("Name") if code.get("Time_Schedule__r") else None,
        "school_name": code.get("Account").get("Name") if code.get("Account") else None,
        "week_name": code.get("Week__r").get("Name") if code.get("Week__r") else None,
        "start_date": code.get("Week__r").get("Start_Date__c") if code.get("Week__r") else None,
        "end_date": code.get("Week__r").get("End_Date__c") if code.get("Week__r") else None,
        "teacher_name": code.get("Teacher__r").get("Full_Name__c") if code.get("Teacher__r") else None,
        "teacher_id": code.get("Teacher__r").get("Id") if code.get("Teacher__r") else None,
        "teacher_uid": code.get("Teacher__r").get("Firebase_UID__c") if code.get("Teacher__r") else None,
        "event_id": code.get("Google_Event__c"),
        "ages": code.get("Ages_Real__c"),
        "stage": code.get("StageName")
    } for code in result]

    return {"data": {"response": codes, "status": 200}}
