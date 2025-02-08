from Helpers import firebase_functions_custom, https_fn_custom
from Salesforce import getSF

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def interviews_a_get_all(data):
    # Initialize DB and SF
    sf = getSF()

    # Get all contracts
    interviews = sf.sf.query_all_iter(f"""
        SELECT FIELDS(ALL)
        FROM Note__c
        WHERE RecordTypeId = '012P5000001UtMf'
        LIMIT 200
        """)

    return {"data": {"response": list(interviews), "status": 200}}
