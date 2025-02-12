from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def replacements_a_get(data):
    # Initialize the Salesforce client
    sf = getSF()

    # Get all results
    results = sf.sf.query_all_iter("""
        SELECT
            Id, CreatedDate, Date__c, RecordTypeId, RecordType.Name,
            Teacher__r.Full_Name__c, Teacher__r.Id,
            Teacher_Old__r.Full_Name__c, Teacher_Old__r.Id,
            Opportunity__r.Code__c, Opportunity__r.Start_Time__c, Opportunity__r.End_Time__c, Opportunity__r.Day_of_Week__c, Opportunity__r.Id
        FROM Replacement__c
        WHERE Opportunity__r.RecordTypeId = '012060000003OPWAA2'
            AND (RecordTypeId = '012P5000001QASzIAO' OR RecordTypeId = '012P5000001QAUbIAO')
            AND Deleted__c = False
    """)

    return {"data": {"response": list(results), "status": 200}}
