from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def reimbursements_a_get(data):
    return getter(f"""
        SELECT
            Id, Name, CreatedDate, Date__c, Amount__c, Justification__c, Attachment__c, Status__c,
            Status_Justification__c, Summary__c, Employee__r.Full_Name__c, Employee__r.Id
        FROM Reimbursement__c
        WHERE RecordType.Name = 'UserRequested'
            AND Deleted__c = False
    """)
