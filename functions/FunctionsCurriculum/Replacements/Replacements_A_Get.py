from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_a_get(data):
    return getter("""
        SELECT
            Id, CreatedDate, Date__c, RecordTypeId, RecordType.Name, Reason__c,
            Teacher__r.Full_Name__c, Teacher__r.Name, Teacher__r.Id,
            Teacher_Old__r.Full_Name__c, Teacher_Old__r.Name, Teacher_Old__r.Id,
            Opportunity__r.Code__c, Opportunity__r.Start_Time__c, Opportunity__r.End_Time__c, Opportunity__r.Day_of_Week__c, Opportunity__r.Id,
            Opportunity__r.Time_Schedule__r.Start_Time__c, Opportunity__r.Time_Schedule__r.End_Time__c
        FROM Replacement__c
        WHERE (RecordTypeId = '012P5000001QASzIAO' OR RecordTypeId = '012P5000001QAUbIAO')
            AND Deleted__c = False
    """)

# Opportunity__r.RecordTypeId = '012060000003OPWAA2'
#             AND
