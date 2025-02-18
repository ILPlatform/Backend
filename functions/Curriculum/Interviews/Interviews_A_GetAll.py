from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def interviews_a_get_all(data):
    return getter("""
        SELECT FIELDS(ALL)
        FROM Note__c
        WHERE RecordTypeId = '012P5000001UtMf'
    """)
