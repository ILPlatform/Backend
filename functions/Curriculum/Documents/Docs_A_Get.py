from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=3)
def docs_a_get(data):
    return getter("""
        SELECT FIELDS(ALL), Teacher__r.Full_Name__c, Teacher__r.Id
        FROM Document__c
        WHERE Deleted__c = False
    """)
