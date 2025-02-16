from Helpers import getter

docs_a_get = getter(lambda data: """
    SELECT FIELDS(ALL), Teacher__r.Full_Name__c, Teacher__r.Id
    FROM Document__c
    WHERE Deleted__c = False
    """, auth_level=3)
