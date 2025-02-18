from Helpers import getter
from Helpers import https_fn_custom, firebase_functions_custom

@https_fn_custom()
@firebase_functions_custom(auth_level=1)
def docs_u_get(data):
    return getter(f"""
        SELECT FIELDS(ALL)
        FROM Document__c
        WHERE Deleted__c = False
            AND Teacher__r.Firebase_UID__c = '{data.get("uid")}'
            AND Signed__c = {data.get("signed")}
    """)
