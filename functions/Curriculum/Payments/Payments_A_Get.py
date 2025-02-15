from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=10)
def payments_a_get(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all payments from SF
    results = list(sf.sf.query_all_iter("""
        SELECT
            FIELDS(ALL), Beneficiary__r.Full_Name__c,
            Document__r.Signed__c, Document__r.Unsigned_URL__c, Document__r.Signed_URL__c
        FROM Payment__c
        WHERE RecordTypeId = '012P5000001tRevIAE' and Deleted__c = False
        LIMIT 200
    """))

    return {"data": {"response": list(results), "status": 200}}
