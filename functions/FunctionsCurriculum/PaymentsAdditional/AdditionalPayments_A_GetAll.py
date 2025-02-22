from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def additional_payments_a_get_all(data):
    return getter("""
        SELECT FIELDS(ALL), Beneficiary__r.Full_Name__c
        FROM Payment__c
        WHERE (RecordTypeId = '012P5000001tcX7IAI' OR RecordTypeId = NULL)
            AND Deleted__c = False
    """)
