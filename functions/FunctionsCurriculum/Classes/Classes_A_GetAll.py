from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def classes_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get the user
    result = sf.sf.query_all_iter(f"""
        SELECT
            Id, Code__c, Day_of_Week__c, Start_Time__c, End_Time__c, Account.Name, Account.Short_Name__c,
            Yearly_Schedule__r.Start_Date__c, Yearly_Schedule__r.End_Date__c,
            Teacher__r.Id, Teacher__r.Full_Name__c, Teacher__r.Firebase_UID__c,
            Google_Event__c, StageName,
            (
                SELECT Teacher__r.Full_Name__c, Date__c, Teacher__r.Id, Teacher__r.Firebase_UID__c
                FROM Replacements__r
                WHERE Deleted__c = False AND RecordTypeId = '012P5000001QAUbIAO'
            )
        FROM Opportunity
        WHERE RecordTypeId = '012060000003OPWAA2'
            AND StageName!='Cancelled'
    """)

    # Get the teacher with the latest date in the replacements
    def get_teacher(code):
        replacements = code.get("Replacements__r").get("records") if code.get("Replacements__r") else None
        if not replacements:
            return [
                code.get("Teacher__r").get("Full_Name__c"),
                code.get("Teacher__r").get("Id"),
                code.get("Teacher__r").get("Firebase_UID__c")
            ] if code.get("Teacher__r") else [None, None, None]
        replacements = sorted(replacements, key=lambda x: x.get("Date__c"), reverse=True)
        return [
            replacements[0].get("Teacher__r").get("Full_Name__c"),
            replacements[0].get("Teacher__r").get("Id"),
            replacements[0].get("Teacher__r").get("Firebase_UID__c")
        ] if replacements[0].get("Teacher__r") else [None, None, None]

    # Process the result
    codes = [{
        "id": code.get("Id"),
        "code": code.get("Code__c"),
        "day_of_week": code.get("Day_of_Week__c"),
        "time": f"{code.get('Start_Time__c')[:5] if code.get('Start_Time__c') else '??'}-{code.get('End_Time__c')[:5] if code.get('End_Time__c') else '??'}",
        "school_name": code.get("Account").get("Name") if code.get("Account") else None,
        "start_date": code.get("Yearly_Schedule__r").get("Start_Date__c") if code.get("Yearly_Schedule__r") else None,
        "end_date": code.get("Yearly_Schedule__r").get("End_Date__c") if code.get("Yearly_Schedule__r") else None,
        "teacher_name": get_teacher(code)[0],
        "teacher_id": get_teacher(code)[1],
        "teacher_uid": get_teacher(code)[2],
        "event_id": code.get("Google_Event__c")
    } | code for code in result]

    return {"data": {"response": codes, "status": 200}}
