from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_a_get(data):
    return getter("""
        SELECT
            FIELDS(ALL), Beneficiary__r.Full_Name__c,
            Document__r.Signed__c, Document__r.Unsigned_URL__c, Document__r.Signed_URL__c
        FROM Payment__c
        WHERE RecordTypeId = '012P5000001tRevIAE' and Deleted__c = False
    """)
