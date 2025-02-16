from Helpers import getter

docs_u_get = getter(lambda data: f"""
    SELECT FIELDS(ALL)
    FROM Document__c
    WHERE Deleted__c = False
        AND Teacher__r.Firebase_UID__c = '{data.get("uid")}'
        AND Signed__c = {data.get("signed")}
    """, auth_level=1)
