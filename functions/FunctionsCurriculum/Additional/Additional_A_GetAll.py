from Helpers import firebase_functions_custom, https_fn_custom, getter

# from Emails.SendEmailReplacementsOneTime import send_email_replacement_onetime, send_email_replacement_onetime_admin

@https_fn_custom()
@firebase_functions_custom(auth_level=2)
def additional_a_get_all(data):
    return getter("""
        SELECT
            Id, CreatedDate, Date__c, RecordTypeId, RecordType.Name,
            Teacher__r.Name, Teacher__r.Last_Name__c, Teacher__r.Id, Teacher__r.Full_Name__c,
            Opportunity__r.Code__c, Opportunity__r.Start_Time__c, Opportunity__r.End_Time__c, Opportunity__r.Account.Name, Opportunity__r.Day_of_Week__c, Opportunity__r.Id
        FROM Replacement__c
        WHERE Opportunity__r.RecordTypeId = '012060000003OPWAA2'
            AND (RecordTypeId = '012P5000001YwypIAC')
            AND Deleted__c = False
    """)
