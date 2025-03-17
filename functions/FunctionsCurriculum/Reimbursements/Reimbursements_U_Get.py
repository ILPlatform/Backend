from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def reimbursements_u_get(data):
    return getter(f"""
        SELECT
            Id, CreatedDate, Date__c, Amount__c, Justification__c, Attachment__c, Status__c,
            Status_Justification__c, Summary__c
        FROM Reimbursement__c
        WHERE Employee__r.Firebase_UID__c = '{data.get("uid")}'
            AND RecordType.Name = 'UserRequested'
            AND Deleted__c = False
    """)
