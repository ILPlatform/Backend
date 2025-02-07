from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def docs_u_get(data):
    # Initialize SF
    sf = getSF()

    # Get all contracts
    documents = sf.sf.query_all_iter(f"""
        SELECT FIELDS(ALL)
        FROM Document__c
        WHERE Deleted__c = False
            AND Teacher__r.Firebase_UID__c = '{data.get("uid")}'
            AND Signed__c = {data.get("signed")}
        LIMIT 200
        """)

    return {"data": {"response": list(documents), "status": 200}}
