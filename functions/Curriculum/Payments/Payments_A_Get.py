from Helpers import getter

payments_a_get = getter(lambda data: """
    SELECT
        FIELDS(ALL), Beneficiary__r.Full_Name__c,
        Document__r.Signed__c, Document__r.Unsigned_URL__c, Document__r.Signed_URL__c
    FROM Payment__c
    WHERE RecordTypeId = '012P5000001tRevIAE' and Deleted__c = False
    """, auth_level=10)
