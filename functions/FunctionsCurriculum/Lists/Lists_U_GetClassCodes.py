from google.cloud.firestore_v1.base_query import FieldFilter
from Helpers import firebase_functions_custom, https_fn_custom
from Google.Connector import GoogleConnector
from firebase_functions import https_fn, options
from datetime import datetime
from firebase_admin import auth
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def lists_u_get_class_codes(data):
    # Get the parameters
    uid = data.get("uid")

    # Initialize DB and SF
    sf = getSF()

    # Get the user
    result_direct = sf.sf.query_all_iter(f"""
        SELECT
            Id, Code__c,
            Day_of_Week__c, Start_Time__c, End_Time__c, Account.Name
        FROM Opportunity
        WHERE Teacher__r.Firebase_UID__c = '{uid}'
    """)
    result_indirect = sf.sf.query_all_iter(f"""
        SELECT
            Id, Code__c, Day_of_Week__c,
            Start_Time__c, End_Time__c, Account.Name
        FROM Opportunity
        WHERE Id IN (
            SELECT Opportunity__c
            FROM Replacement__c
            WHERE (Teacher__r.Firebase_UID__c = '{uid}'
                OR Teacher_Old__r.Firebase_UID__c = '{uid}')
                AND Deleted__c = False
        )
    """)

    # Process the result
    codes = [code | {
        "id": code.get("Id"),
        "code": code.get("Code__c"),
        "day_of_week": code.get("Day_of_Week__c"),
        "description": f"{code.get('Code__c')} [{code.get('Account').get('Name')} - {code.get('Day_of_Week__c')} - {code.get('Start_Time__c')[:5] if code.get('Start_Time__c') else '??'}-{code.get('End_Time__c')[:5] if code.get('End_Time__c') else '??'}]",
        "time": f"{code.get('Start_Time__c')[:5] if code.get('Start_Time__c') else '??'}-{code.get('End_Time__c')[:5] if code.get('End_Time__c') else '??'}"
    } for code in list(result_direct) + list(result_indirect)]

    return {"data": {"response": codes, "status": 200}}
