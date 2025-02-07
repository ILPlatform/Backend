from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_get_all(data):
    # Initialize SF
    sf = getSF()

    # Get all contracts
    documents = sf.sf.query_all_iter(f"""
        SELECT FIELDS(ALL), Teacher__r.Full_Name__c, Teacher__r.Id
        FROM Document__c
        WHERE Deleted__c = False
        LIMIT 200
        """)

    return {"data": {"response": list(documents), "status": 200}}
